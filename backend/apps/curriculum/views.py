import re
from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.common.permissions import IsAuthorOrAdmin
from .models import Track, Subject
from .serializers import (
    TrackSerializer, TrackDetailSerializer,
    SubjectListSerializer, SubjectDetailSerializer,
)


def _slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


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
    permission_classes = [IsAuthorOrAdmin]

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

        track = Track(
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
        track.save()
        return Response(TrackSerializer(track, context={'admin': True}).data, status=status.HTTP_201_CREATED)


class AdminTrackDetailView(APIView):
    permission_classes = [IsAuthorOrAdmin]

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
        if 'slug' in request.data:
            new_slug = request.data['slug'].strip()
            if new_slug != slug and Track.objects(slug=new_slug).first():
                return Response({'slug': 'A track with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            track.slug = new_slug

        track.updated_at = datetime.now(timezone.utc)
        track.save()
        return Response(TrackSerializer(track, context={'admin': True}).data)

    def delete(self, request, slug):
        track = Track.objects(slug=slug).first()
        if not track:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminSubjectListView(APIView):
    permission_classes = [IsAuthorOrAdmin]

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
    permission_classes = [IsAuthorOrAdmin]

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
        if 'slug' in request.data:
            new_slug = request.data['slug'].strip()
            if new_slug != slug and Subject.objects(slug=new_slug).first():
                return Response({'slug': 'A subject with this slug already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            subject.slug = new_slug

        subject.updated_at = datetime.now(timezone.utc)
        subject.save()
        return Response(SubjectListSerializer(subject, context={'admin': True}).data)

    def delete(self, request, slug):
        subject = Subject.objects(slug=slug).first()
        if not subject:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
