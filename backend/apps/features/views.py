import re
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import section_required
from apps.users.models import User
from .models import FeatureFlag
from .registry import FEATURE_REGISTRY, get_spec
from .service import effective_flags

AUDIENCES = ('all', 'selected')


def _is_object_id(value):
    try:
        ObjectId(str(value))
        return True
    except (InvalidId, TypeError):
        return False


def _admin_row(flag, spec=None):
    spec = spec or get_spec(flag.key) or {}
    return {
        'key': flag.key,
        'label': flag.label or spec.get('label', flag.key),
        'description': flag.description or spec.get('description', ''),
        'owner_section': spec.get('owner_section', ''),
        'enabled': flag.enabled,
        'audience': flag.audience,
        'allowed_user_ids': list(flag.allowed_user_ids or []),
        'allowed_user_count': len(flag.allowed_user_ids or []),
        'updated_at': flag.updated_at.isoformat() if flag.updated_at else None,
    }


class EffectiveFlagsView(APIView):
    """Learner-facing: the resolved {key: bool} map for the current user.

    Returns ONLY the boolean map — never allowed_user_ids (don't leak who is in
    a beta cohort). Works for anonymous users too.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(effective_flags(request.user))


class AdminFeatureFlagListView(APIView):
    permission_classes = [section_required('features')]

    def get(self, request):
        # Materialize a row per registry key so the admin always sees a full grid
        # (self-heals if seed_feature_flags hasn't been run for a new key).
        rows = []
        for spec in FEATURE_REGISTRY:
            flag = FeatureFlag.get_or_create(spec['key'])
            rows.append(_admin_row(flag, spec))
        return Response(rows)


class FeatureUserSearchView(APIView):
    """Minimal user lookup for the 'selected users' picker — keeps the Feature
    Flags admin self-contained (doesn't require the separate 'users' section).
    Returns only id/email/username/full_name. Resolves explicit ids too, so the
    picker can render the names of already-selected users."""
    permission_classes = [section_required('features')]

    def get(self, request):
        ids = request.query_params.get('ids', '').strip()
        if ids:
            wanted = [i for i in (s.strip() for s in ids.split(',')) if _is_object_id(i)]
            users = User.objects(id__in=wanted) if wanted else []
        else:
            q = request.query_params.get('q', '').strip()
            qs = User.objects
            if q:
                qs = qs.filter(__raw__={'$or': [
                    {'email':     {'$regex': re.escape(q), '$options': 'i'}},
                    {'username':  {'$regex': re.escape(q), '$options': 'i'}},
                    {'full_name': {'$regex': re.escape(q), '$options': 'i'}},
                ]})
            users = qs.order_by('email').limit(20)
        return Response([
            {'id': str(u.id), 'email': u.email, 'username': u.username, 'full_name': u.full_name}
            for u in users
        ])


class AdminFeatureFlagDetailView(APIView):
    permission_classes = [section_required('features')]

    def patch(self, request, key):
        if not get_spec(key):
            return Response({'detail': 'Unknown feature key.'}, status=status.HTTP_404_NOT_FOUND)
        flag = FeatureFlag.get_or_create(key)
        data = request.data

        if 'enabled' in data:
            flag.enabled = bool(data['enabled'])

        if 'audience' in data:
            audience = (data['audience'] or '').strip()
            if audience not in AUDIENCES:
                return Response({'audience': "Must be 'all' or 'selected'."}, status=status.HTTP_400_BAD_REQUEST)
            flag.audience = audience

        if 'allowed_user_ids' in data:
            raw = data['allowed_user_ids']
            if not isinstance(raw, list):
                return Response({'allowed_user_ids': 'Must be a list.'}, status=status.HTTP_400_BAD_REQUEST)
            # Keep only well-formed ObjectIds that map to a real user; dedupe.
            valid, seen = [], set()
            for item in raw:
                sid = str(item).strip()
                if sid in seen or not _is_object_id(sid):
                    continue
                if User.objects(id=sid).first():
                    seen.add(sid)
                    valid.append(sid)
            flag.allowed_user_ids = valid

        flag.updated_at = datetime.now(timezone.utc)
        flag.save()
        return Response(_admin_row(flag))
