import re
from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.common.permissions import IsAuthorOrAdmin
from apps.curriculum.models import Subject
from .models import Lesson, ContentBlock
from .serializers import LessonDetailSerializer, LessonListSerializer


def _slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


# ── Public read ──────────────────────────────────────────────────────────────

class LessonDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        from apps.progress.models import UserProgress

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

        enrolled = False
        if is_auth and track_slug:
            up = UserProgress.objects(user=request.user).first()
            enrolled = bool(up and track_slug in (up.enrolled_tracks or []))

        context = {
            'truncate': not is_auth,
            'needs_enrollment': is_auth and not enrolled and bool(track_slug),
            'track_slug': track_slug,
            'track_title': track_title,
        }
        return Response(LessonDetailSerializer(lesson, context=context).data)


# ── Admin CRUD ───────────────────────────────────────────────────────────────

class AdminLessonListView(APIView):
    permission_classes = [IsAuthorOrAdmin]

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

        blocks = []
        for i, raw in enumerate(request.data.get('content_blocks') or []):
            block_type = raw.get('type', '')
            if block_type not in ('text', 'verse', 'hadith', 'image', 'video', 'quiz'):
                return Response(
                    {'content_blocks': f'Invalid block type "{block_type}" at index {i}.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            blocks.append(ContentBlock(type=block_type, order=i, body=raw.get('body', {})))

        lesson = Lesson(
            subject=subject,
            title=title,
            slug=slug,
            summary=request.data.get('summary', ''),
            order=int(request.data.get('order', 0)),
            estimated_minutes=int(request.data.get('estimated_minutes', 0)),
            status=lesson_status,
            content_blocks=blocks,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        lesson.save()
        return Response(AdminLessonSerializer(lesson).data, status=status.HTTP_201_CREATED)


class AdminLessonDetailView(APIView):
    permission_classes = [IsAuthorOrAdmin]

    def get(self, request, slug):
        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(AdminLessonSerializer(lesson).data)

    def patch(self, request, slug):
        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        for field in ('title', 'summary'):
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
            blocks = []
            for i, raw in enumerate(request.data['content_blocks']):
                block_type = raw.get('type', '')
                if block_type not in ('text', 'verse', 'hadith', 'image', 'video', 'quiz'):
                    return Response(
                        {'content_blocks': f'Invalid block type "{block_type}" at index {i}.'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                blocks.append(ContentBlock(type=block_type, order=i, body=raw.get('body', {})))
            lesson.content_blocks = blocks

        lesson.updated_at = datetime.now(timezone.utc)
        lesson.save()
        return Response(AdminLessonSerializer(lesson).data)

    def delete(self, request, slug):
        lesson = Lesson.objects(slug=slug).first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        lesson.delete()
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

    def get_subject_slug(self, obj):
        return obj.subject.slug

    def get_subject_title(self, obj):
        return obj.subject.title

    def get_content_blocks(self, obj):
        return [
            {'type': b.type, 'order': b.order, 'body': b.body}
            for b in sorted(obj.content_blocks, key=lambda b: b.order)
        ]
