"""Admin panel API: user management, per-user activity, and role/permission CRUD.

All endpoints are gated by section (`users` or `roles`) via `section_required`.
Lives under /api/v1/auth/admin/ (see urls.py).
"""
import re
from datetime import datetime, timezone

from mongoengine.errors import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.common.permissions import SECTIONS, section_required, any_section_required
from apps.progress.models import LessonProgress, QuizAttempt, UserProgress
from .models import User, Role, _SYSTEM_ROLE_SECTIONS

SECTION_LABELS = {
    'curriculum': 'Curriculum',
    'library': 'Library',
    'videos': 'Videos',
    'users': 'Users',
    'analytics': 'Analytics',
    'roles': 'Roles & Permissions',
    'registrations': 'Registrations',
}

ACTIVITY_LIMIT = 100


def _iso(dt):
    return dt.isoformat() if dt else None


def _role_names_with_section(section):
    """Role names (incl. built-in fallbacks) whose grant includes `section`."""
    names = {name for name, secs in _SYSTEM_ROLE_SECTIONS.items() if section in secs}
    for r in Role.objects():
        secs = list(SECTIONS) if r.name == 'admin' else (r.sections or [])
        if section in secs:
            names.add(r.name)
    return names


def _count_active_section_holders(section, exclude_id=None):
    qs = User.objects(role__in=list(_role_names_with_section(section)), is_active=True)
    if exclude_id:
        qs = qs.filter(id__ne=exclude_id)
    return qs.count()


def _role_is_valid(name):
    return bool(Role.objects(name=name).first()) or name in _SYSTEM_ROLE_SECTIONS


def _get_user(user_id):
    try:
        return User.objects(id=user_id).first()
    except (ValidationError, Exception):
        return None


# ── Users ──────────────────────────────────────────────────────────────────

class AdminUserListView(APIView):
    permission_classes = [section_required('users')]

    def get(self, request):
        qs = User.objects
        q = request.query_params.get('q', '').strip()
        role = request.query_params.get('role', '').strip()
        active = request.query_params.get('active', '').strip().lower()
        if q:
            qs = qs.filter(__raw__={'$or': [
                {'email':     {'$regex': re.escape(q), '$options': 'i'}},
                {'username':  {'$regex': re.escape(q), '$options': 'i'}},
                {'full_name': {'$regex': re.escape(q), '$options': 'i'}},
            ]})
        if role:
            qs = qs.filter(role=role)
        if active in ('true', 'false'):
            qs = qs.filter(is_active=(active == 'true'))

        users = list(qs.order_by('-created_at'))

        # Two aggregate passes (raw ids, no per-user dereference) instead of N queries.
        completions = {
            str(r['_id']): r['c']
            for r in LessonProgress.objects.aggregate([
                {'$match': {'completed': True}},
                {'$group': {'_id': '$user', 'c': {'$sum': 1}}},
            ])
        }
        streaks = {
            str(r['user']): r
            for r in UserProgress.objects.aggregate(
                [{'$project': {'user': 1, 'current_streak_days': 1, 'last_activity_date': 1}}]
            )
        }

        data = []
        for u in users:
            uid = str(u.id)
            up = streaks.get(uid)
            data.append({
                'id': uid,
                'email': u.email,
                'username': u.username,
                'full_name': u.full_name,
                'role': u.role,
                'is_active': u.is_active,
                'is_verified': u.is_verified,
                'lessons_completed': completions.get(uid, 0),
                'current_streak': (up.get('current_streak_days') if up else 0) or 0,
                'last_activity': _iso(up.get('last_activity_date')) if up and up.get('last_activity_date') else None,
                'last_login': _iso(u.last_login),
                'created_at': _iso(u.created_at),
            })
        return Response(data)


class AdminUserDetailView(APIView):
    permission_classes = [section_required('users')]

    def get(self, request, user_id):
        u = _get_user(user_id)
        if not u:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        up = UserProgress.objects(user=u).first()
        return Response({
            'id': str(u.id),
            'email': u.email,
            'username': u.username,
            'full_name': u.full_name,
            'role': u.role,
            'sections': u.get_sections(),
            'is_active': u.is_active,
            'is_verified': u.is_verified,
            'last_login': _iso(u.last_login),
            'created_at': _iso(u.created_at),
            'lessons_completed': LessonProgress.objects(user=u, completed=True).count(),
            'current_streak': up.current_streak_days if up else 0,
            'longest_streak': up.longest_streak_days if up else 0,
            'enrolled_tracks': (up.enrolled_tracks if up else []) or [],
        })

    def patch(self, request, user_id):
        u = _get_user(user_id)
        if not u:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        is_self = str(u.id) == str(request.user.id)

        if 'role' in request.data:
            new_role = (request.data['role'] or '').strip()
            if not _role_is_valid(new_role):
                return Response({'role': 'Unknown role.'}, status=status.HTTP_400_BAD_REQUEST)
            # Guard: don't strip the last admin's access by reassigning them.
            losing_users = 'users' in u.get_sections() and 'users' not in (
                list(SECTIONS) if new_role == 'admin' else
                (Role.objects(name=new_role).first().sections if Role.objects(name=new_role).first() else _SYSTEM_ROLE_SECTIONS.get(new_role, []))
            )
            if losing_users and _count_active_section_holders('users', exclude_id=u.id) == 0:
                return Response({'role': 'Cannot remove the last user with Users access.'}, status=status.HTTP_400_BAD_REQUEST)
            u.role = new_role

        if 'is_active' in request.data:
            new_active = bool(request.data['is_active'])
            if not new_active:
                if is_self:
                    return Response({'is_active': 'You cannot deactivate your own account.'}, status=status.HTTP_400_BAD_REQUEST)
                if 'users' in u.get_sections() and _count_active_section_holders('users', exclude_id=u.id) == 0:
                    return Response({'is_active': 'Cannot deactivate the last user with Users access.'}, status=status.HTTP_400_BAD_REQUEST)
            u.is_active = new_active

        u.save()
        return Response({'id': str(u.id), 'role': u.role, 'is_active': u.is_active})

    def delete(self, request, user_id):
        u = _get_user(user_id)
        if not u:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        if str(u.id) == str(request.user.id):
            return Response({'detail': 'You cannot delete your own account.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'users' in u.get_sections() and _count_active_section_holders('users', exclude_id=u.id) == 0:
            return Response({'detail': 'Cannot delete the last user with Users access.'}, status=status.HTTP_400_BAD_REQUEST)
        u.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminUserPasswordView(APIView):
    permission_classes = [section_required('users')]

    def post(self, request, user_id):
        u = _get_user(user_id)
        if not u:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        password = request.data.get('password') or ''
        if len(password) < 8:
            return Response({'password': 'Password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)
        u.set_password(password)
        u.save()
        return Response({'detail': 'Password updated.'})


class AdminUserActivityView(APIView):
    permission_classes = [section_required('users')]

    def get(self, request, user_id):
        u = _get_user(user_id)
        if not u:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        events = []
        for lp in LessonProgress.objects(user=u, completed=True).order_by('-completed_at').limit(ACTIVITY_LIMIT):
            events.append({
                'type': 'lesson_completed',
                'at': lp.completed_at,
                'lesson_slug': lp.lesson_slug,
                'track_slug': lp.track_slug,
            })
        for qa in QuizAttempt.objects(user=u).order_by('-attempted_at').limit(ACTIVITY_LIMIT):
            events.append({
                'type': 'quiz_attempt',
                'at': qa.attempted_at,
                'lesson_slug': qa.lesson_slug,
                'question': qa.question,
                'is_correct': qa.is_correct,
                'selected_answer': qa.selected_answer,
            })
        if u.last_login:
            events.append({'type': 'login', 'at': u.last_login})
        events.append({'type': 'registered', 'at': u.created_at})

        events = [e for e in events if e['at']]
        events.sort(key=lambda e: e['at'], reverse=True)
        for e in events:
            e['at'] = _iso(e['at'])

        # Per-track completed counts (denormalized track_slug on progress).
        track_counts = {}
        for lp in LessonProgress.objects(user=u, completed=True):
            track_counts[lp.track_slug or '—'] = track_counts.get(lp.track_slug or '—', 0) + 1

        return Response({
            'events': events[:ACTIVITY_LIMIT],
            'tracks': [{'track_slug': k, 'completed_lessons': v} for k, v in sorted(track_counts.items())],
        })


# ── Roles & Permissions ──────────────────────────────────────────────────────

def _role_payload(r):
    return {
        'id': str(r.id),
        'name': r.name,
        'label': r.label or r.name.capitalize(),
        'description': r.description or '',
        'sections': r.sections or [],
        'is_system': r.is_system,
        'user_count': User.objects(role=r.name).count(),
    }


def _clean_sections(raw):
    return [s for s in (raw or []) if s in SECTIONS]


class RoleListView(APIView):
    # Reading roles is allowed for user managers too (to populate the role
    # picker); creating roles still requires the `roles` section (checked below).
    permission_classes = [any_section_required(['roles', 'users'])]

    def get(self, request):
        roles = Role.objects.order_by('-is_system', 'name')
        return Response([_role_payload(r) for r in roles])

    def post(self, request):
        if 'roles' not in request.user.get_sections():
            return Response({'detail': 'You do not have access to manage roles.'}, status=status.HTTP_403_FORBIDDEN)
        name = (request.data.get('name') or '').strip().lower()
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{1,49}', name):
            return Response({'name': 'Use 2–50 chars: lowercase letters, numbers, hyphen or underscore.'}, status=status.HTTP_400_BAD_REQUEST)
        if name in _SYSTEM_ROLE_SECTIONS or Role.objects(name=name).first():
            return Response({'name': 'A role with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        role = Role(
            name=name,
            label=(request.data.get('label') or name.capitalize()).strip(),
            description=(request.data.get('description') or '').strip(),
            sections=_clean_sections(request.data.get('sections')),
            is_system=False,
        )
        role.save()
        return Response(_role_payload(role), status=status.HTTP_201_CREATED)


class RoleDetailView(APIView):
    permission_classes = [section_required('roles')]

    def _get(self, role_id):
        try:
            return Role.objects(id=role_id).first()
        except (ValidationError, Exception):
            return None

    def patch(self, request, role_id):
        role = self._get(role_id)
        if not role:
            return Response({'detail': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
        if role.is_system:
            return Response({'detail': 'Built-in roles cannot be edited.'}, status=status.HTTP_403_FORBIDDEN)
        if 'label' in request.data:
            role.label = (request.data['label'] or '').strip()
        if 'description' in request.data:
            role.description = (request.data['description'] or '').strip()
        if 'sections' in request.data:
            role.sections = _clean_sections(request.data['sections'])
        role.save()
        return Response(_role_payload(role))

    def delete(self, request, role_id):
        role = self._get(role_id)
        if not role:
            return Response({'detail': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
        if role.is_system:
            return Response({'detail': 'Built-in roles cannot be deleted.'}, status=status.HTTP_403_FORBIDDEN)
        in_use = User.objects(role=role.name).count()
        if in_use:
            return Response(
                {'detail': f'{in_use} user(s) still have this role. Reassign them first.'},
                status=status.HTTP_409_CONFLICT,
            )
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SectionListView(APIView):
    """The catalogue of grantable sections, for the role editor UI."""
    permission_classes = [section_required('roles')]

    def get(self, request):
        return Response([{'key': s, 'label': SECTION_LABELS.get(s, s.capitalize())} for s in SECTIONS])
