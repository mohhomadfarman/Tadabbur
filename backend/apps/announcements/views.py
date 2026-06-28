from datetime import datetime, timezone

from mongoengine.errors import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import section_required
from apps.lessons.models import ContentBlock
from apps.lessons.views import _normalize_blocks  # shared block validation
from .models import Announcement, AnnouncementView


def _iso(dt):
    return dt.isoformat() if dt else None


def _parse_dt(val):
    """Parse an ISO string (incl. 'YYYY-MM-DDTHH:MM' from datetime-local) → datetime/None."""
    if not val or not isinstance(val, str):
        return None
    try:
        return datetime.fromisoformat(val.replace('Z', '+00:00'))
    except ValueError:
        return None


def _blocks(a):
    return [
        {'type': b.type, 'order': b.order, 'body': b.body}
        for b in sorted(a.content_blocks, key=lambda b: b.order)
    ]


def _public(a):
    return {'id': str(a.id), 'title': a.title, 'content_blocks': _blocks(a)}


def _admin_row(a, with_blocks=False):
    views = AnnouncementView.objects(announcement=a).count()
    dismissed = AnnouncementView.objects(announcement=a, dismissed=True).count()
    data = {
        'id': str(a.id),
        'title': a.title,
        'is_active': a.is_active,
        'starts_at': _iso(a.starts_at),
        'ends_at': _iso(a.ends_at),
        'priority': a.priority,
        'views': views,
        'dismissed': dismissed,
        'block_count': len(a.content_blocks),
        'created_at': _iso(a.created_at),
        'updated_at': _iso(a.updated_at),
    }
    if with_blocks:
        data['content_blocks'] = _blocks(a)
    return data


def _get(announcement_id):
    try:
        return Announcement.objects(id=announcement_id).first()
    except (ValidationError, Exception):
        return None


# ── Learner-facing ───────────────────────────────────────────────────────────

class ActiveAnnouncementsView(APIView):
    """Active, in-window announcements the current user has not seen yet."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Raw ObjectIds of announcements this user has already seen (no dereference).
        seen = set(
            str(aid) for aid in
            AnnouncementView._get_collection().distinct('announcement', {'user': request.user.id})
        )
        now = datetime.now(timezone.utc)
        result = []
        for a in Announcement.objects(is_active=True).order_by('-priority', '-created_at'):
            if str(a.id) in seen or not a.is_live(now):
                continue
            result.append(_public(a))
        return Response(result)


class RecordViewView(APIView):
    """Mark an announcement seen by the current user (idempotent) — drives analytics."""
    permission_classes = [IsAuthenticated]

    def post(self, request, announcement_id):
        a = _get(announcement_id)
        if not a:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        view = AnnouncementView.objects(user=request.user, announcement=a).first()
        if not view:
            try:
                AnnouncementView(user=request.user, announcement=a,
                                 viewed_at=datetime.now(timezone.utc)).save()
            except Exception:
                pass  # unique-index race — already recorded
        return Response({'viewed': True})


class DismissView(APIView):
    """Record that the user explicitly closed the modal (close-rate analytics)."""
    permission_classes = [IsAuthenticated]

    def post(self, request, announcement_id):
        a = _get(announcement_id)
        if not a:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        view = AnnouncementView.objects(user=request.user, announcement=a).first()
        if not view:
            view = AnnouncementView(user=request.user, announcement=a)
        view.dismissed = True
        view.dismissed_at = datetime.now(timezone.utc)
        view.save()
        return Response({'dismissed': True})


# ── Admin CRUD ───────────────────────────────────────────────────────────────

class AdminAnnouncementListView(APIView):
    permission_classes = [section_required('announcements')]

    def get(self, request):
        qs = Announcement.objects.order_by('-priority', '-created_at')
        return Response([_admin_row(a) for a in qs])

    def post(self, request):
        title = (request.data.get('title') or '').strip()
        if not title:
            return Response({'title': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        normalized, error = _normalize_blocks(request.data.get('content_blocks') or [])
        if error:
            return Response({'content_blocks': error}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now(timezone.utc)
        a = Announcement(
            title=title,
            content_blocks=[ContentBlock(type=b['type'], order=b['order'], body=b['body']) for b in normalized],
            is_active=bool(request.data.get('is_active', False)),
            starts_at=_parse_dt(request.data.get('starts_at')),
            ends_at=_parse_dt(request.data.get('ends_at')),
            priority=int(request.data.get('priority', 0) or 0),
            created_at=now,
            updated_at=now,
        )
        a.save()
        return Response(_admin_row(a, with_blocks=True), status=status.HTTP_201_CREATED)


class AdminAnnouncementDetailView(APIView):
    permission_classes = [section_required('announcements')]

    def get(self, request, announcement_id):
        a = _get(announcement_id)
        if not a:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(_admin_row(a, with_blocks=True))

    def patch(self, request, announcement_id):
        a = _get(announcement_id)
        if not a:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if 'title' in request.data:
            a.title = (request.data['title'] or '').strip()
        if 'is_active' in request.data:
            a.is_active = bool(request.data['is_active'])
        if 'priority' in request.data:
            a.priority = int(request.data['priority'] or 0)
        if 'starts_at' in request.data:
            a.starts_at = _parse_dt(request.data['starts_at'])
        if 'ends_at' in request.data:
            a.ends_at = _parse_dt(request.data['ends_at'])
        if 'content_blocks' in request.data:
            normalized, error = _normalize_blocks(request.data['content_blocks'])
            if error:
                return Response({'content_blocks': error}, status=status.HTTP_400_BAD_REQUEST)
            a.content_blocks = [
                ContentBlock(type=b['type'], order=b['order'], body=b['body']) for b in normalized
            ]

        a.updated_at = datetime.now(timezone.utc)
        a.save()
        return Response(_admin_row(a, with_blocks=True))

    def delete(self, request, announcement_id):
        a = _get(announcement_id)
        if not a:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        a.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
