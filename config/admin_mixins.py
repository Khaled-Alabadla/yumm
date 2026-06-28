"""Shared permission helpers for Yumm admin ModelAdmin classes."""


class SiteOwnerPermissionMixin:
    """
    Differentiates Site Owner (is_superuser) from Regular Admin (is_staff).

    Regular admins can view and moderate records but cannot delete them.
    Only superusers receive delete permission.
    """

    def _is_site_owner(self, request) -> bool:
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None) -> bool:
        return self._is_site_owner(request)
