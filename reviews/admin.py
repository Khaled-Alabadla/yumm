"""Django admin configuration for the reviews app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from config.admin_mixins import SiteOwnerPermissionMixin

from .models import CommentReply, Notification, Review, ReviewImage, Wishlist


# ---------------------------------------------------------------------------
# Bulk actions — review moderation
# ---------------------------------------------------------------------------

@admin.action(description=_("Mark selected reviews as resolved (clear report flag)"))
def resolve_reported_reviews(modeladmin, request, queryset):
    updated = queryset.update(is_reported=False)
    modeladmin.message_user(
        request,
        ngettext(
            "%(count)d review was marked as resolved.",
            "%(count)d reviews were marked as resolved.",
            updated,
        )
        % {"count": updated},
    )


@admin.action(description=_("Hide selected reviews from the public site"))
def hide_reviews(modeladmin, request, queryset):
    updated = queryset.update(is_visible=False)
    modeladmin.message_user(
        request,
        ngettext(
            "%(count)d review was hidden.",
            "%(count)d reviews were hidden.",
            updated,
        )
        % {"count": updated},
    )


@admin.action(description=_("Restore selected reviews to the public site"))
def show_reviews(modeladmin, request, queryset):
    updated = queryset.update(is_visible=True)
    modeladmin.message_user(
        request,
        ngettext(
            "%(count)d review was restored.",
            "%(count)d reviews were restored.",
            updated,
        )
        % {"count": updated},
    )


# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0
    fields = ("image", "order", "uploaded_at")
    readonly_fields = ("uploaded_at",)


class CommentReplyInline(admin.TabularInline):
    model = CommentReply
    extra = 0
    fields = ("user", "reply_text", "created_at")
    readonly_fields = ("created_at",)


# ---------------------------------------------------------------------------
# Review admin
# ---------------------------------------------------------------------------

@admin.register(Review)
class ReviewAdmin(SiteOwnerPermissionMixin, admin.ModelAdmin):
    """
    Review moderation.

    Regular admins: view, search, filter reported reviews, hide/resolve them.
    Site owner: full CRUD including permanent deletion.
    """

    list_display = (
        "restaurant",
        "user",
        "rating",
        "is_reported",
        "is_visible",
        "created_at",
    )
    list_filter = (
        "is_reported",
        "is_visible",
        "rating",
        ("created_at", admin.DateFieldListFilter),
    )
    search_fields = (
        "comment",
        "user__email",
        "user__first_name",
        "user__last_name",
        "restaurant__name_ar",
        "restaurant__name_en",
    )
    list_select_related = ("user", "restaurant")
    date_hierarchy = "created_at"
    inlines = (ReviewImageInline, CommentReplyInline)
    actions = (resolve_reported_reviews, hide_reviews, show_reviews)

    fieldsets = (
        (
            None,
            {"fields": ("user", "restaurant", "rating", "comment")},
        ),
        (
            _("Moderation"),
            {"fields": ("is_reported", "is_visible")},
        ),
        (
            _("Timestamps"),
            {"fields": ("created_at", "updated_at")},
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        """Regular admins may only change moderation fields."""
        if self._is_site_owner(request):
            return self.readonly_fields
        return [
            field.name
            for field in self.model._meta.fields
            if field.name not in ("is_reported", "is_visible")
        ]

    def has_add_permission(self, request) -> bool:
        return self._is_site_owner(request)

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff


# ---------------------------------------------------------------------------
# Supporting admins
# ---------------------------------------------------------------------------

@admin.register(Wishlist)
class WishlistAdmin(SiteOwnerPermissionMixin, admin.ModelAdmin):
    list_display = ("user", "restaurant", "created_at")
    search_fields = ("user__email", "restaurant__name_en", "restaurant__name_ar")
    list_select_related = ("user", "restaurant")

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_add_permission(self, request) -> bool:
        return self._is_site_owner(request)


@admin.register(Notification)
class NotificationAdmin(SiteOwnerPermissionMixin, admin.ModelAdmin):
    list_display = ("user", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read")
    search_fields = ("text_ar", "text_en", "user__email")

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_add_permission(self, request) -> bool:
        return self._is_site_owner(request)
