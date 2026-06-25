"""Custom DRF permission classes based on the user's role.

Usage in any APIView or ViewSet:
    permission_classes = [IsAuthenticated, IsAdminRole]
    permission_classes = [IsAuthenticated, IsOwnerRole]
    permission_classes = [IsAuthenticated, IsAdminOrOwnerRole]
"""

from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Allows access only to users with role == 'admin'."""

    message = _("Admin access required.")

    def has_permission(self, request, view) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_admin_role
        )


class IsOwnerRole(BasePermission):
    """Allows access only to users with role == 'owner'."""

    message = _("Owner access required.")

    def has_permission(self, request, view) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_owner_role
        )


class IsAdminOrOwnerRole(BasePermission):
    """Allows access to users with role == 'admin' or 'owner'."""

    message = _("Admin or Owner access required.")

    def has_permission(self, request, view) -> bool:
        return request.user and request.user.is_authenticated and (
            request.user.is_admin_role or request.user.is_owner_role
        )


class IsSelfOrAdminRole(BasePermission):
    """
    Object-level permission: allow only the resource owner or an admin.

    The view must call `self.get_object()` to trigger this check.
    """

    message = _("You do not have permission to perform this action.")

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.is_admin_role or obj == request.user
