"""Django admin configuration for the accounts app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.action(description=_("Approve selected restaurant owners"))
def approve_owners(modeladmin, request, queryset):
    from restaurants.owner_sync import sync_restaurants_for_owner

    owner_ids = list(
        queryset.filter(role=CustomUser.Role.OWNER).values_list("pk", flat=True)
    )
    updated = CustomUser.objects.filter(pk__in=owner_ids).update(
        is_approved=True,
        is_active=True,
    )
    for owner in CustomUser.objects.filter(pk__in=owner_ids):
        sync_restaurants_for_owner(owner)
    modeladmin.message_user(
        request,
        _("%(count)d owner account(s) approved.") % {"count": updated},
    )


@admin.action(description=_("Reject selected restaurant owners"))
def reject_owners(modeladmin, request, queryset):
    updated = queryset.filter(role=CustomUser.Role.OWNER).update(
        is_approved=False,
        is_active=False,
    )
    modeladmin.message_user(
        request,
        _("%(count)d owner account(s) rejected.") % {"count": updated},
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    User management — accessible only to the Site Owner (is_superuser).

    Regular admins (is_staff, not superuser) cannot view or manage
    other admin profiles.
    """

    ordering = ("email",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "approval_status",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )
    list_filter = ("role", "is_approved", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    actions = (approve_owners, reject_owners)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "role", "is_approved")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                    "is_approved",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    @admin.display(description=_("Approval status"))
    def approval_status(self, obj):
        if not obj.is_owner_role:
            return "—"
        if obj.is_approved:
            return format_html(
                '<span style="color:#28a745;font-weight:600;">{}</span>',
                _("Approved"),
            )
        return format_html(
            '<span style="color:#ffc107;font-weight:600;">{}</span>',
            _("Pending approval"),
        )

    # ------------------------------------------------------------------
    # Site Owner only — block all access for regular staff admins
    # ------------------------------------------------------------------

    def has_module_permission(self, request) -> bool:
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser

    def has_add_permission(self, request) -> bool:
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser
