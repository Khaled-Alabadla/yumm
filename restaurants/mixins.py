"""Shared mixins for the restaurant-owner dashboard."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.utils.translation import get_language_bidi, gettext_lazy as _

from accounts.decorators import OwnerRequiredMixin

from .forms import MenuItemForm
from .models import MenuCategory, MenuItem, Restaurant, RestaurantCategory
from reviews.models import Review
from .utils import is_open_now


class ApprovedOwnerMixin(OwnerRequiredMixin):
    """Owner role required; pending owners are sent to the approval page."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_pending_owner:
            return redirect("accounts:pending")
        return super().dispatch(request, *args, **kwargs)


class RestaurantOwnerMixin(ApprovedOwnerMixin):
    """
    Resolve the restaurant owned by the current user.

    In DEBUG mode, a demo restaurant is created automatically for the
    demo owner account so the dashboard can be explored without admin setup.
    """

    active_tab = "overview"
    restaurant = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_pending_owner:
            return redirect("accounts:pending")

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        from django.core.exceptions import PermissionDenied

        if not request.user.is_owner_role:
            raise PermissionDenied(_("Owner access required."))

        self.restaurant = (
            Restaurant.objects.filter(owner=request.user)
            .select_related("category")
            .first()
        )

        if not self.restaurant and settings.DEBUG:
            self.restaurant = _ensure_demo_restaurant(request.user)

        if not self.restaurant:
            return render(
                request,
                "restaurants/dashboard/no_restaurant.html",
                {"page_title": _("Restaurant Dashboard")},
            )

        return super(ApprovedOwnerMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurant"] = self.restaurant
        context["active_tab"] = self.active_tab
        context["page_title"] = _("Restaurant Dashboard")
        context["is_open_now"] = is_open_now(self.restaurant)
        return context

    def get_menu_swal_i18n(self) -> dict:
        """Translated strings for SweetAlert dialogs on the menu page."""
        return {
            "deleteTitle": str(_("Delete menu item?")),
            "deleteText": str(_("This action cannot be undone.")),
            "confirmDelete": str(_("Yes, delete")),
            "cancel": str(_("Cancel")),
            "deleted": str(_("Deleted!")),
            "deleteFailed": str(_("Could not delete this item.")),
            "ok": str(_("OK")),
        }

    def get_menu_page_context(self, **extra):
        """Shared context for the menu tab and menu-item POST handlers."""
        menu_items = (
            self.restaurant.menu_items.select_related("category")
            .order_by("order", "name_en")
        )
        context = {
            "restaurant": self.restaurant,
            "active_tab": "menu",
            "page_title": _("Restaurant Dashboard"),
            "is_open_now": is_open_now(self.restaurant),
            "page_is_rtl": get_language_bidi(),
            "menu_swal_i18n": self.get_menu_swal_i18n(),
            "menu_items": menu_items,
            "item_form": MenuItemForm(),
            "edit_forms": {
                item.pk: MenuItemForm(instance=item) for item in menu_items
            },
            "show_add_modal": False,
        }
        context.update(extra)
        return context


def _ensure_demo_restaurant(user) -> Restaurant | None:
    """Create a sample restaurant for demo owner accounts (DEBUG only)."""
    if not user.is_owner_role:
        return None

    existing = Restaurant.objects.filter(owner=user).first()
    if existing:
        return existing

    category, _ = RestaurantCategory.objects.get_or_create(
        name_en="Traditional Palestinian",
        defaults={"name_ar": "فلسطيني تقليدي", "order": 0},
    )

    restaurant = Restaurant.objects.create(
        owner=user,
        category=category,
        name_en="Al-Kanaan",
        name_ar="الكنعان",
        description_en=(
            "Authentic Palestinian cuisine in the heart of Ramallah."
        ),
        description_ar="مطبخ فلسطيني أصيل في قلب رام الله.",
        address_en="Al-Masyoun, Ramallah, Palestine",
        address_ar="الماصيون، رام الله، فلسطين",
        city=Restaurant.City.RAMALLAH,
        working_hours_en="11:00 - 23:00",
        working_hours_ar="11:00 - 23:00",
        is_open=True,
        status=Restaurant.Status.ACTIVE,
    )

    menu_category, _ = MenuCategory.objects.get_or_create(
        restaurant=restaurant,
        name_en="Main Dishes",
        defaults={"name_ar": "الأطباق الرئيسية", "order": 0},
    )

    demo_items = [
        (
            "Musakhan",
            "مسخن",
            "Roasted chicken on taboon bread with caramelised sumac onions.",
            "45.00",
        ),
        (
            "Mansaf",
            "منسف",
            "Slow-cooked lamb in fermented jameed sauce on a bed of saffron rice.",
            "65.00",
        ),
        (
            "Maqluba",
            "مقلوبة",
            "Upside-down layered rice with chicken, aubergine and toasted nuts.",
            "55.00",
        ),
        (
            "Knafeh",
            "كنافة",
            "Shredded pastry layered with sweet white cheese, soaked in rose-water syrup.",
            "18.00",
        ),
    ]

    for order, (name_en, name_ar, desc_en, price) in enumerate(demo_items):
        MenuItem.objects.get_or_create(
            restaurant=restaurant,
            name_en=name_en,
            defaults={
                "category": menu_category,
                "name_ar": name_ar,
                "description_en": desc_en,
                "description_ar": desc_en,
                "price": price,
                "order": order,
            },
        )

    if not restaurant.reviews.exists():
        User = get_user_model()
        demo_reviewers = [
            ("Layla", "Hassan", 5, "Amazing musakhan! Best I've had in Ramallah."),
            ("Omar", "Khalil", 4, "Excellent food and great portions. The mansaf was authentic."),
            ("Sara", "Al-Ahmad", 5, "A hidden gem! Every dish perfectly seasoned."),
        ]
        for first, last, rating, comment in demo_reviewers:
            reviewer, _ = User.objects.get_or_create(
                email=f"demo.{first.lower()}@yumm.ps",
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "role": User.Role.USER,
                    "is_approved": True,
                },
            )
            Review.objects.get_or_create(
                user=reviewer,
                restaurant=restaurant,
                defaults={"rating": rating, "comment": comment},
            )

    return restaurant
