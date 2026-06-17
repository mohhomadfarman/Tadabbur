from rest_framework.permissions import BasePermission

AUTHOR_ROLES = {'author', 'scholar', 'admin'}


class IsAuthorOrAdmin(BasePermission):
    """Allows access only to users with an authoring role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) in AUTHOR_ROLES
        )
