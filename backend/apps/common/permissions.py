from rest_framework.permissions import BasePermission

# The unit of access control. A Role grants a subset of these; holding a section
# means view + edit within that section of the admin panel / API.
SECTIONS = ['curriculum', 'library', 'videos', 'users', 'analytics', 'roles', 'registrations', 'translations', 'announcements', 'features', 'feedback', 'badges', 'email', 'automations']


def _user_sections(user):
    if not (user and getattr(user, 'is_authenticated', False)):
        return set()
    getter = getattr(user, 'get_sections', None)
    return set(getter()) if getter else set()


def section_required(section):
    """DRF permission: allow only users whose role grants `section`."""
    class _SectionPermission(BasePermission):
        def has_permission(self, request, view):
            return section in _user_sections(request.user)
    return _SectionPermission


def any_section_required(sections):
    """DRF permission: allow if the user holds ANY of `sections`."""
    wanted = set(sections)

    class _AnySectionPermission(BasePermission):
        def has_permission(self, request, view):
            return bool(wanted & _user_sections(request.user))
    return _AnySectionPermission


# Back-compat alias for any imports still referencing the old coarse gate. Means
# "can author content" (curriculum/library/videos). Specific views are gated to
# their exact section below.
IsAuthorOrAdmin = any_section_required(['curriculum', 'library', 'videos'])
