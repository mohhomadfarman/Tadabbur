import re
from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.common.permissions import section_required
from apps.curriculum.models import Subject
from .models import Lesson, ContentBlock
from .serializers import LessonDetailSerializer, LessonListSerializer

BLOCK_TYPES = ('text', 'verse', 'hadith', 'image', 'video', 'quiz')


def _slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def _normalize_blocks(raw_list):
    """Validate incoming content blocks; returns (list_of_dicts, error_message)."""
    blocks = []
    for i, raw in enumerate(raw_list or []):
        block_type = (raw.get('type') or '')
        if block_type not in BLOCK_TYPES:
            return None, f'Invalid block type "{block_type}" at index {i}.'
        blocks.append({'type': block_type, 'order': i, 'body': raw.get('body', {}) or {}})
    return blocks, None


# ── Public read ──────────────────────────────────────────────────────────────

class LessonDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        from apps.progress.models import UserProgress
        from apps.translations.models import TranslationSettings

        lesson = Lesson.objects(slug=slug, status='published').first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        is_auth = bool(request.user and request.user.is_authenticated)

        track_slug = ''
        track_title = ''
        try:
            track_slug = lesson.subject.track.slug
            track_title = lesson.subject.track.title
        except Exception:
            pass

        up = UserProgress.objects(user=request.user).first() if is_auth else None
        enrolled = bool(up and track_slug and track_slug in (up.enrolled_tracks or []))

        # ── Resolve the active translation ────────────────────────────────────
        # Only languages still enabled by admins are offered in the switcher, but
        # an existing translation is served if explicitly requested or preferred.
        settings_doc = TranslationSettings.get_solo()
        enabled = {l.code: l for l in settings_doc.enabled_languages()}
        lesson_translations = lesson.translations or {}
        available_languages = [
            {'code': l.code, 'name': l.name, 'native_name': l.native_name or '', 'rtl': bool(l.rtl)}
            for code, l in enabled.items() if code in lesson_translations
        ]

        requested = (request.query_params.get('lang') or '').strip()
        pref = (up.track_languages or {}).get(track_slug, '') if (up and track_slug) else ''
        active_lang = requested or pref
        translation = lesson_translations.get(active_lang) if active_lang else None
        if translation is None:
            active_lang = ''  # falling back to the original

        context = {
            'truncate': not is_auth,
            'needs_enrollment': is_auth and not enrolled and bool(track_slug),
            'track_slug': track_slug,
            'track_title': track_title,
            'translation': translation,
            'active_lang': active_lang,
            'available_languages': available_languages,
        }
        return Response(LessonDetailSerializer(lesson, context=context).data)


# ── Admin CRUD ───────────────────────────────────────────────────────────────

class AdminLessonListView(APIView):
    permission_classes = [section_required('curriculum')]

    def get(self, request):
        subject_slug = request.query_params.get('subject')
        if not subject_slug:
            return Response({'detail': 'subject query param required.'}, status=status.HTTP_400_BAD_REQUEST)
        subject = Subject.objects(slug=subject_slug).first()
        if not subject:
            return Response({'detail': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)
        lessons = Lesson.objects(subject=subject).order_by('order')
        return Response(AdminLessonListSerializer(lessons, many=True).data)

    def post(self, request):
        subject_slug = (request.data.get('subject_slug') or '').strip()
        title = (request.data.get('title') or '').strip()
        if not subject_slug or not title:
            return Response({'detail': 'subject_slug and title are required.'}, status=status.HTTP_400_BAD_REQUEST)

        subject = Subject.objects(slug=subject_slug).first()
        if not subject:
            return Response({'subject_slug': 'Subject not found.'}, status=status.HTTP_400_BAD_REQUEST)

        slug = (request.data.get('slug') or _slugify(title)).strip()
        if Lesson.objects(slug=slug).first():
            return Response({'slug': 'A lesson with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        raw_status = request.data.get('status', 'draft')
        lesson_status = raw_status if raw_status in ('draft', 'published') else 'draft'

        normalized, error = _normalize_blocks(request.data.get('content_blocks') or [])
        if error:
            return Response({'content_blocks': error}, status=status.HTTP_400_BAD_REQUEST)
        blocks = [ContentBlock(type=b['type'], order=b['order'], body=b['body']) for b in normalized]

        lesson = Lesson(
            subject=subject,
            title=title,
            slug=slug,
            summary=request.data.get('summary', ''),
            order=int(request.data.get('order', 0)),
            estimated_minutes=int(request.data.get('estimated_minutes', 0)),
            status=lesson_status,
            content_blocks=blocks,
            meta_title=request.data.get('meta_title', ''),
            meta_description=request.data.get('meta_description', ''),
            og_image=request.data.get('og_image', ''),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        lesson.save()
        return Response(AdminLessonSerializer(lesson).data, status=status.HTTP_201_CREATED)


class AdminLessonDetailView(APIView):
    permission_classes = [section_required('curriculum')]

    def get(self, request, slug):
        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(AdminLessonSerializer(lesson).data)

    def patch(self, request, slug):
        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        for field in ('title', 'summary', 'meta_title', 'meta_description', 'og_image'):
            if field in request.data:
                setattr(lesson, field, request.data[field])
        if 'estimated_minutes' in request.data:
            lesson.estimated_minutes = int(request.data['estimated_minutes'])
        if 'order' in request.data:
            lesson.order = int(request.data['order'])
        if 'status' in request.data and request.data['status'] in ('draft', 'published'):
            lesson.status = request.data['status']
        if 'slug' in request.data:
            new_slug = request.data['slug'].strip()
            if new_slug != slug and Lesson.objects(slug=new_slug).first():
                return Response({'slug': 'A lesson with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            lesson.slug = new_slug

        # Replace entire content_blocks list when provided
        if 'content_blocks' in request.data:
            normalized, error = _normalize_blocks(request.data['content_blocks'])
            if error:
                return Response({'content_blocks': error}, status=status.HTTP_400_BAD_REQUEST)
            lesson.content_blocks = [
                ContentBlock(type=b['type'], order=b['order'], body=b['body']) for b in normalized
            ]

        lesson.updated_at = datetime.now(timezone.utc)
        lesson.save()
        return Response(AdminLessonSerializer(lesson).data)

    def delete(self, request, slug):
        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Admin translation (generate / save / delete) ─────────────────────────────

class AdminLessonTranslateView(APIView):
    """Generate a translation candidate with Gemini. Does NOT persist — the author
    reviews/edits, then saves via AdminLessonTranslationDetailView (PUT)."""
    permission_classes = [section_required('curriculum')]

    def post(self, request, slug):
        from apps.translations.models import TranslationSettings
        from apps.translations.services import translate_lesson, GeminiNotConfigured, GeminiError

        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        code = (request.data.get('language') or '').strip()
        if not code:
            return Response({'language': 'language code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        settings_doc = TranslationSettings.get_solo()
        language = settings_doc.find_language(code)
        if not language:
            return Response({'language': f'Unknown language "{code}".'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            candidate = translate_lesson(lesson, language, settings_doc)
        except GeminiNotConfigured:
            return Response({'detail': 'Gemini is not configured. Add an API key in Admin → Languages.'}, status=503)
        except GeminiError as exc:
            return Response({'detail': str(exc)}, status=502)

        return Response({'language': code, 'translation': candidate})


class AdminLessonTranslationDetailView(APIView):
    """Save (PUT) or remove (DELETE) a reviewed translation on a lesson."""
    permission_classes = [section_required('curriculum')]

    def put(self, request, slug, code):
        from apps.translations.models import TranslationSettings

        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        code = (code or '').strip()
        settings_doc = TranslationSettings.get_solo()
        if not settings_doc.find_language(code):
            return Response({'language': f'Unknown language "{code}".'}, status=status.HTTP_400_BAD_REQUEST)

        normalized, error = _normalize_blocks(request.data.get('content_blocks') or [])
        if error:
            return Response({'content_blocks': error}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now(timezone.utc)
        entry = {
            'title': request.data.get('title', '') or '',
            'summary': request.data.get('summary', '') or '',
            'meta_title': request.data.get('meta_title', '') or '',
            'meta_description': request.data.get('meta_description', '') or '',
            'content_blocks': normalized,
            'source_updated_at': lesson.updated_at.isoformat() if lesson.updated_at else now.isoformat(),
            'translated_at': now.isoformat(),
            'model': settings_doc.model,
            'edited': bool(request.data.get('edited', False)),
        }
        translations = dict(lesson.translations or {})
        translations[code] = entry
        lesson.translations = translations
        lesson.save()
        return Response({'language': code, 'translation': entry})

    def delete(self, request, slug, code):
        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        translations = dict(lesson.translations or {})
        if code in translations:
            del translations[code]
            lesson.translations = translations
            lesson.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Admin-only serializers (inline to keep files minimal) ───────────────────

from rest_framework import serializers


class AdminLessonListSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title = serializers.CharField()
    slug = serializers.CharField()
    summary = serializers.CharField()
    order = serializers.IntegerField()
    estimated_minutes = serializers.IntegerField()
    status = serializers.CharField()
    block_count = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.id)

    def get_block_count(self, obj):
        return len(obj.content_blocks)


class AdminLessonSerializer(AdminLessonListSerializer):
    subject_slug = serializers.SerializerMethodField()
    subject_title = serializers.SerializerMethodField()
    content_blocks = serializers.SerializerMethodField()
    translations = serializers.SerializerMethodField()
    meta_title = serializers.CharField(default='')
    meta_description = serializers.CharField(default='')
    og_image = serializers.CharField(default='')

    def get_subject_slug(self, obj):
        return obj.subject.slug

    def get_subject_title(self, obj):
        return obj.subject.title

    def get_content_blocks(self, obj):
        return [
            {'type': b.type, 'order': b.order, 'body': b.body}
            for b in sorted(obj.content_blocks, key=lambda b: b.order)
        ]

    def get_translations(self, obj):
        """Full translations dict, each annotated with `is_outdated` (original edited
        after the translation was generated)."""
        lesson_iso = obj.updated_at.isoformat() if obj.updated_at else ''
        out = {}
        for code, tr in (obj.translations or {}).items():
            src = tr.get('source_updated_at') or ''
            out[code] = {**tr, 'is_outdated': bool(src and lesson_iso and src < lesson_iso)}
        return out
