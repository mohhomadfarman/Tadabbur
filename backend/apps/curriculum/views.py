import re
from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.common.permissions import section_required
from config.redirects import record_slug_redirect
from .models import Track, Subject, Category, Level
from .serializers import (
    TrackSerializer, TrackDetailSerializer,
    SubjectListSerializer, SubjectDetailSerializer,
)


def _slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def _category_row(c):
    return {
        'id': str(c.id),
        'title': c.title,
        'slug': c.slug,
        'order': c.order,
        'levels': [{'name': l.name, 'slug': l.slug, 'order': l.order} for l in c.levels],
    }


def _build_levels(raw_list):
    """Convert a list of {name, slug?, order?} dicts into embedded Level
    documents. Auto-slugifies missing slugs; rejects duplicate slugs within
    the list (returns (None, error_message) on failure)."""
    levels = []
    seen_slugs = set()
    for i, raw in enumerate(raw_list or [], start=1):
        if not isinstance(raw, dict):
            continue
        name = (raw.get('name') or '').strip()
        if not name:
            continue
        slug = (raw.get('slug') or _slugify(name)).strip()
        if slug in seen_slugs:
            return None, f'Duplicate level slug "{slug}".'
        seen_slugs.add(slug)
        levels.append(Level(name=name, slug=slug, order=int(raw.get('order', i))))
    return levels, None


# ── Public read ──────────────────────────────────────────────────────────────

class TrackListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tracks = Track.objects(is_published=True).order_by('order')
        return Response(TrackSerializer(tracks, many=True).data)


class TrackDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        track = Track.objects(slug=slug, is_published=True).first()
        if not track:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(TrackDetailSerializer(track).data)


class SubjectDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        subject = Subject.objects(slug=slug, is_published=True).first()
        if not subject:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SubjectDetailSerializer(subject).data)


# ── Admin: list all content (incl. drafts) ───────────────────────────────────

class AdminTrackListView(APIView):
    permission_classes = [section_required('curriculum')]

    def get(self, request):
        tracks = Track.objects.order_by('order')
        return Response(TrackSerializer(tracks, many=True, context={'admin': True}).data)

    def post(self, request):
        title = (request.data.get('title') or '').strip()
        if not title:
            return Response({'title': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        slug = (request.data.get('slug') or _slugify(title)).strip()
        if Track.objects(slug=slug).first():
            return Response({'slug': 'A track with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        category = None
        category_slug = (request.data.get('category_slug') or '').strip()
        if category_slug:
            category = Category.objects(slug=category_slug).first()
            if not category:
                return Response({'category_slug': 'Category not found.'}, status=status.HTTP_400_BAD_REQUEST)
        level_slug = (request.data.get('level_slug') or '').strip()
        if level_slug and (not category or not any(l.slug == level_slug for l in category.levels)):
            return Response({'level_slug': 'Level does not belong to the selected category.'}, status=status.HTTP_400_BAD_REQUEST)

        track = Track(
            title=title,
            slug=slug,
            description=request.data.get('description', ''),
            thumbnail_url=request.data.get('thumbnail_url', ''),
            order=int(request.data.get('order', 0)),
            is_published=False,
            category=category,
            level_slug=level_slug,
            meta_title=request.data.get('meta_title', ''),
            meta_description=request.data.get('meta_description', ''),
            og_image=request.data.get('og_image', ''),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        track.save()
        return Response(TrackSerializer(track, context={'admin': True}).data, status=status.HTTP_201_CREATED)


class AdminTrackDetailView(APIView):
    permission_classes = [section_required('curriculum')]

    def get(self, request, slug):
        track = Track.objects(slug=slug).first()
        if not track:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(TrackDetailSerializer(track, context={'admin': True}).data)

    def patch(self, request, slug):
        track = Track.objects(slug=slug).first()
        if not track:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        for field in ('title', 'description', 'thumbnail_url', 'meta_title', 'meta_description', 'og_image'):
            if field in request.data:
                setattr(track, field, request.data[field])
        if 'order' in request.data:
            track.order = int(request.data['order'])
        if 'is_published' in request.data:
            track.is_published = bool(request.data['is_published'])
        if 'category_slug' in request.data or 'level_slug' in request.data:
            category_slug = (request.data.get('category_slug') or '').strip()
            category = Category.objects(slug=category_slug).first() if category_slug else None
            if category_slug and not category:
                return Response({'category_slug': 'Category not found.'}, status=status.HTTP_400_BAD_REQUEST)
            level_slug = (request.data.get('level_slug') or '').strip()
            if level_slug and (not category or not any(l.slug == level_slug for l in category.levels)):
                return Response({'level_slug': 'Level does not belong to the selected category.'}, status=status.HTTP_400_BAD_REQUEST)
            track.category = category
            track.level_slug = level_slug
        old_slug = track.slug
        if 'slug' in request.data:
            new_slug = request.data['slug'].strip()
            if new_slug != slug and Track.objects(slug=new_slug).first():
                return Response({'slug': 'A track with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            track.slug = new_slug

        track.updated_at = datetime.now(timezone.utc)
        track.save()

        if track.slug != old_slug:
            record_slug_redirect(f'/learn/{old_slug}', f'/learn/{track.slug}')
            # Subject URLs embed the parent track's slug, so every subject
            # under this track needs its own redirect too.
            for subject in Subject.objects(track=track):
                record_slug_redirect(
                    f'/learn/{old_slug}/{subject.slug}',
                    f'/learn/{track.slug}/{subject.slug}',
                )

        return Response(TrackSerializer(track, context={'admin': True}).data)

    def delete(self, request, slug):
        track = Track.objects(slug=slug).first()
        if not track:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminSubjectListView(APIView):
    permission_classes = [section_required('curriculum')]

    def get(self, request):
        track_slug = request.query_params.get('track')
        qs = Subject.objects
        if track_slug:
            track = Track.objects(slug=track_slug).first()
            if track:
                qs = Subject.objects(track=track)
        return Response(SubjectListSerializer(qs.order_by('order'), many=True, context={'admin': True}).data)

    def post(self, request):
        track_slug = (request.data.get('track_slug') or '').strip()
        title = (request.data.get('title') or '').strip()
        if not track_slug or not title:
            return Response({'detail': 'track_slug and title are required.'}, status=status.HTTP_400_BAD_REQUEST)

        track = Track.objects(slug=track_slug).first()
        if not track:
            return Response({'track_slug': 'Track not found.'}, status=status.HTTP_400_BAD_REQUEST)

        slug = (request.data.get('slug') or _slugify(title)).strip()
        if Subject.objects(slug=slug).first():
            return Response({'slug': 'A subject with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        subject = Subject(
            track=track,
            title=title,
            slug=slug,
            description=request.data.get('description', ''),
            thumbnail_url=request.data.get('thumbnail_url', ''),
            order=int(request.data.get('order', 0)),
            is_published=False,
            meta_title=request.data.get('meta_title', ''),
            meta_description=request.data.get('meta_description', ''),
            og_image=request.data.get('og_image', ''),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        subject.save()
        return Response(SubjectListSerializer(subject, context={'admin': True}).data, status=status.HTTP_201_CREATED)


class AdminSubjectDetailView(APIView):
    permission_classes = [section_required('curriculum')]

    def get(self, request, slug):
        subject = Subject.objects(slug=slug).first()
        if not subject:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SubjectDetailSerializer(subject, context={'admin': True}).data)

    def patch(self, request, slug):
        subject = Subject.objects(slug=slug).first()
        if not subject:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        for field in ('title', 'description', 'thumbnail_url', 'meta_title', 'meta_description', 'og_image'):
            if field in request.data:
                setattr(subject, field, request.data[field])
        if 'order' in request.data:
            subject.order = int(request.data['order'])
        if 'is_published' in request.data:
            subject.is_published = bool(request.data['is_published'])
        old_slug = subject.slug
        if 'slug' in request.data:
            new_slug = request.data['slug'].strip()
            if new_slug != slug and Subject.objects(slug=new_slug).first():
                return Response({'slug': 'A subject with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            subject.slug = new_slug

        subject.updated_at = datetime.now(timezone.utc)
        subject.save()

        if subject.slug != old_slug:
            track_slug = subject.track.slug
            record_slug_redirect(f'/learn/{track_slug}/{old_slug}', f'/learn/{track_slug}/{subject.slug}')

        return Response(SubjectListSerializer(subject, context={'admin': True}).data)

    def delete(self, request, slug):
        subject = Subject.objects(slug=slug).first()
        if not subject:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminCategoryListView(APIView):
    permission_classes = [section_required('curriculum')]

    def get(self, request):
        return Response([_category_row(c) for c in Category.objects.order_by('order')])

    def post(self, request):
        title = (request.data.get('title') or '').strip()
        if not title:
            return Response({'title': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        slug = (request.data.get('slug') or _slugify(title)).strip()
        if Category.objects(slug=slug).first():
            return Response({'slug': 'A category with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        levels, error = _build_levels(request.data.get('levels'))
        if error:
            return Response({'levels': error}, status=status.HTTP_400_BAD_REQUEST)

        category = Category(
            title=title,
            slug=slug,
            order=int(request.data.get('order', 0)),
            levels=levels,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        category.save()
        return Response(_category_row(category), status=status.HTTP_201_CREATED)


class AdminCategoryDetailView(APIView):
    permission_classes = [section_required('curriculum')]

    def get(self, request, slug):
        category = Category.objects(slug=slug).first()
        if not category:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(_category_row(category))

    def patch(self, request, slug):
        category = Category.objects(slug=slug).first()
        if not category:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if 'title' in request.data:
            category.title = (request.data['title'] or '').strip()
        if 'order' in request.data:
            category.order = int(request.data['order'])
        if 'slug' in request.data:
            new_slug = request.data['slug'].strip()
            if new_slug != slug and Category.objects(slug=new_slug).first():
                return Response({'slug': 'A category with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            category.slug = new_slug

        if 'levels' in request.data:
            new_levels, error = _build_levels(request.data['levels'])
            if error:
                return Response({'levels': error}, status=status.HTTP_400_BAD_REQUEST)
            new_slugs = {lvl.slug for lvl in new_levels}
            removed_slugs = {lvl.slug for lvl in category.levels} - new_slugs
            for removed in removed_slugs:
                if Track.objects(category=category, level_slug=removed).count():
                    return Response(
                        {'levels': f'Level "{removed}" is still assigned to a track — reassign it first.'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            category.levels = new_levels

        category.updated_at = datetime.now(timezone.utc)
        category.save()
        return Response(_category_row(category))

    def delete(self, request, slug):
        category = Category.objects(slug=slug).first()
        if not category:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        if Track.objects(category=category).count():
            return Response(
                {'detail': 'This category still has tracks assigned — reassign them first.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
