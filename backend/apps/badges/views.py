from datetime import datetime, timezone

from mongoengine.errors import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import section_required
from apps.features.service import feature_enabled
from apps.users.models import User
from .models import Badge, UserBadge, CRITERIA_TYPES
from .awards import grant_badge


def _iso(dt):
    return dt.isoformat() if dt else None


def _slug(text):
    import re
    return re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')


def _badge_public(b):
    return {
        'id': str(b.id),
        'key': b.key,
        'name': b.name,
        'description': b.description,
        'icon_url': b.icon_url,
        'reward': b.reward,
    }


def _awarded_payload(ub):
    b = ub.badge
    return {**_badge_public(b), 'awarded_at': _iso(ub.awarded_at), 'seen': ub.seen}


def _admin_row(b):
    return {
        'id': str(b.id),
        'key': b.key,
        'name': b.name,
        'description': b.description,
        'icon_url': b.icon_url,
        'criteria_type': b.criteria_type,
        'criteria_value': b.criteria_value,
        'reward': b.reward,
        'is_active': b.is_active,
        'awarded_count': UserBadge.objects(badge=b).count(),
        'created_at': _iso(b.created_at),
        'updated_at': _iso(b.updated_at),
    }


def _get_badge(badge_id):
    try:
        return Badge.objects(id=badge_id).first()
    except (ValidationError, Exception):
        return None


# ── Learner-facing ───────────────────────────────────────────────────────────

class MyBadgesView(APIView):
    """All badges the current user has earned (for the dashboard/profile)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        awarded = UserBadge.objects(user=request.user).order_by('-awarded_at').select_related()
        return Response([_awarded_payload(ub) for ub in awarded if ub.badge])


class UnseenBadgesView(APIView):
    """Badges awarded but not yet shown in the celebration popup."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not feature_enabled('badges', request.user):
            return Response([])
        unseen = UserBadge.objects(user=request.user, seen=False).order_by('awarded_at')
        return Response([_awarded_payload(ub) for ub in unseen if ub.badge])


class MarkBadgeSeenView(APIView):
    """Mark an awarded badge's popup as shown (idempotent)."""
    permission_classes = [IsAuthenticated]

    def post(self, request, badge_id):
        b = _get_badge(badge_id)
        if not b:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        ub = UserBadge.objects(user=request.user, badge=b).first()
        if ub and not ub.seen:
            ub.seen = True
            ub.save()
        return Response({'seen': True})


# ── Admin CRUD ───────────────────────────────────────────────────────────────

class AdminBadgeListView(APIView):
    permission_classes = [section_required('badges')]

    def get(self, request):
        return Response([_admin_row(b) for b in Badge.objects.order_by('-created_at')])

    def post(self, request):
        name = (request.data.get('name') or '').strip()
        if not name:
            return Response({'name': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        key = _slug(request.data.get('key') or '') or _slug(name)
        if not key:
            return Response({'key': 'Could not derive a key from the name.'}, status=status.HTTP_400_BAD_REQUEST)
        if Badge.objects(key=key).first():
            return Response({'key': 'A badge with this key already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        criteria_type = (request.data.get('criteria_type') or 'manual').strip()
        if criteria_type not in CRITERIA_TYPES:
            return Response({'criteria_type': 'Invalid criteria type.'}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now(timezone.utc)
        b = Badge(
            key=key,
            name=name,
            description=(request.data.get('description') or '').strip(),
            icon_url=(request.data.get('icon_url') or '').strip(),
            criteria_type=criteria_type,
            criteria_value=(request.data.get('criteria_value') or '').strip(),
            reward=(request.data.get('reward') or '').strip(),
            is_active=bool(request.data.get('is_active', True)),
            created_at=now,
            updated_at=now,
        )
        b.save()
        return Response(_admin_row(b), status=status.HTTP_201_CREATED)


class AdminBadgeDetailView(APIView):
    permission_classes = [section_required('badges')]

    def get(self, request, badge_id):
        b = _get_badge(badge_id)
        if not b:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(_admin_row(b))

    def patch(self, request, badge_id):
        b = _get_badge(badge_id)
        if not b:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        d = request.data
        if 'name' in d:
            b.name = (d['name'] or '').strip()
        if 'description' in d:
            b.description = (d['description'] or '').strip()
        if 'icon_url' in d:
            b.icon_url = (d['icon_url'] or '').strip()
        if 'criteria_type' in d:
            ct = (d['criteria_type'] or 'manual').strip()
            if ct not in CRITERIA_TYPES:
                return Response({'criteria_type': 'Invalid criteria type.'}, status=status.HTTP_400_BAD_REQUEST)
            b.criteria_type = ct
        if 'criteria_value' in d:
            b.criteria_value = (d['criteria_value'] or '').strip()
        if 'reward' in d:
            b.reward = (d['reward'] or '').strip()
        if 'is_active' in d:
            b.is_active = bool(d['is_active'])
        b.updated_at = datetime.now(timezone.utc)
        b.save()
        return Response(_admin_row(b))

    def delete(self, request, badge_id):
        b = _get_badge(badge_id)
        if not b:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        b.delete()  # cascades UserBadge rows
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminGrantBadgeView(APIView):
    """Manually award a badge to a user by id (useful for 'manual' badges)."""
    permission_classes = [section_required('badges')]

    def post(self, request, badge_id):
        b = _get_badge(badge_id)
        if not b:
            return Response({'detail': 'Badge not found.'}, status=status.HTTP_404_NOT_FOUND)
        user_id = (request.data.get('user_id') or '').strip()
        try:
            user = User.objects(id=user_id).first()
        except (ValidationError, Exception):
            user = None
        if not user:
            return Response({'user_id': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
        grant_badge(user, b)
        return Response({'granted': True, 'awarded_count': UserBadge.objects(badge=b).count()})
