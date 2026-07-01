"""Django admin configuration for the restaurants app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from config.admin_filters import RecentCreatedFilter
from config.admin_mixins import SiteOwnerPermissionMixin
from config.dashboard import get_platform_stats

from .models import (
    MenuCategory,
    MenuItem,
    Restaurant,
    RestaurantCategory,
    RestaurantImage,
    Tag,
)

# ---------------------------------------------------------------------------
# Bulk actions
# ---------------------------------------------------------------------------

@admin.action(description=_("Approve selected restaurants"))
def approve_restaurants(modeladmin, request, queryset):
    updated = 0
    for restaurant in queryset.select_related("owner"):
        restaurant.status = Restaurant.Status.ACTIVE
        restaurant.is_open = True
        restaurant.save(update_fields=["status", "is_open", "updated_at"])
        updated += 1
    modeladmin.message_user(
        request,
        ngettext(
            "%(count)d restaurant was approved.",
            "%(count)d restaurants were approved.",
            updated,
        )
        % {"count": updated},
    )


@admin.action(description=_("Reject selected restaurants"))
def reject_restaurants(modeladmin, request, queryset):
    updated = 0
    for restaurant in queryset.select_related("owner"):
        restaurant.status = Restaurant.Status.REJECTED
        restaurant.is_open = False
        restaurant.save(update_fields=["status", "is_open", "updated_at"])
        updated += 1
    modeladmin.message_user(
        request,
        ngettext(
            "%(count)d restaurant was rejected.",
            "%(count)d restaurants were rejected.",
            updated,
        )
        % {"count": updated},
    )


# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------

class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1
    fields = ("image", "image_type", "is_primary", "caption_en", "caption_ar", "order")


class MenuCategoryInline(admin.TabularInline):
    model = MenuCategory
    extra = 0
    fields = ("name_en", "name_ar", "order")


# ---------------------------------------------------------------------------
# Restaurant admin
# ---------------------------------------------------------------------------

@admin.register(Restaurant)
class RestaurantAdmin(SiteOwnerPermissionMixin, admin.ModelAdmin):
    """
    Restaurant management with role-based permissions.

    Regular admins: view, search, filter, approve/reject via status or actions.
    Site owner: full CRUD including permanent deletion.
    """

    change_list_template = "admin/restaurants/restaurant/change_list.html"

    list_display = ("display_name", "owner", "status", "city", "created_at")
    list_filter = ("status", "city", "is_open", RecentCreatedFilter)
    search_fields = (
        "name_ar",
        "name_en",
        "description_ar",
        "description_en",
        "address_ar",
        "address_en",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    )
    list_select_related = ("owner",)
    filter_horizontal = ("tags",)
    inlines = (RestaurantImageInline, MenuCategoryInline)
    actions = (approve_restaurants, reject_restaurants)

    fieldsets = (
        (
            _("Ownership & status"),
            {"fields": ("owner", "status", "is_open", "category", "tags")},
        ),
        (
            _("Identity"),
            {"fields": ("name_ar", "name_en", "description_ar", "description_en")},
        ),
        (
            _("Location"),
            {
                "fields": (
                    "address_ar",
                    "address_en",
                    "city",
                    "latitude",
                    "longitude",
                ),
            },
        ),
        (
            _("Hours & pricing"),
            {
                "fields": (
                    "working_hours_ar",
                    "working_hours_en",
                    "price_range",
                ),
            },
        ),
    )

    @admin.display(description=_("name"))
    def display_name(self, obj: Restaurant) -> str:
        return obj.name_en or obj.name_ar

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["platform_stats"] = get_platform_stats()
        return super().changelist_view(request, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        """Regular admins may only change the approval status field."""
        if self._is_site_owner(request):
            return ()
        readonly = [
            field.name
            for field in self.model._meta.fields
            if field.name != "status"
        ]
        readonly.append("tags")
        return readonly

    def get_inlines(self, request, obj):
        """Only the Site Owner can manage images and menu categories inline."""
        if self._is_site_owner(request):
            return self.inlines
        return ()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_staff:
            return {}
        return actions

    def has_add_permission(self, request) -> bool:
        return self._is_site_owner(request)

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff


# ---------------------------------------------------------------------------
# Supporting model admins (Site Owner only for destructive ops)
# ---------------------------------------------------------------------------

@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(SiteOwnerPermissionMixin, admin.ModelAdmin):
    list_display = ("name_en", "name_ar", "order")
    search_fields = ("name_en", "name_ar")
    ordering = ("order", "name_en")

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_add_permission(self, request) -> bool:
        return self._is_site_owner(request)


@admin.register(Tag)
class TagAdmin(SiteOwnerPermissionMixin, admin.ModelAdmin):
    list_display = ("name_en", "name_ar")
    search_fields = ("name_en", "name_ar")

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_add_permission(self, request) -> bool:
        return self._is_site_owner(request)


@admin.register(MenuItem)
class MenuItemAdmin(SiteOwnerPermissionMixin, admin.ModelAdmin):
    list_display = ("name_en", "restaurant", "category", "price", "is_available")
    list_filter = ("is_available", "restaurant")
    search_fields = ("name_ar", "name_en", "restaurant__name_en", "restaurant__name_ar")
    list_select_related = ("restaurant", "category")

    def has_module_permission(self, request) -> bool:
        return request.user.is_staff

    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_change_permission(self, request, obj=None) -> bool:
        return request.user.is_staff

    def has_add_permission(self, request) -> bool:
        return self._is_site_owner(request)
