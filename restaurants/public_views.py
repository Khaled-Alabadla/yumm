"""Public restaurant browsing views."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import DetailView, ListView
from urllib.parse import urlencode

from reviews.forms import ReviewForm
from reviews.models import Review, Wishlist

from .geo import get_all_city_choices
from .models import Restaurant
from .querysets import (
    FEATURED_CITY_CODES,
    annotate_public_stats,
    get_filter_categories,
    get_map_restaurants,
    get_public_restaurant_detail,
    get_public_restaurant_list,
    get_rating_breakdown,
    get_top_rated_restaurants,
)
from .utils import is_open_now


class RestaurantListView(ListView):
    """Browse active restaurants with search, city, and cuisine filters."""

    template_name = "restaurants/list.html"
    context_object_name = "restaurants"
    paginate_by = 12

    def get_queryset(self):
        self.q = self.request.GET.get("q", "").strip()
        self.city = self.request.GET.get("city", "").strip()
        self.category_id = self.request.GET.get("category", "").strip()
        try:
            self.active_category_id = int(self.category_id) if self.category_id else None
        except ValueError:
            self.active_category_id = None
        self.filtered_queryset = get_public_restaurant_list(
            q=self.q,
            city=self.city,
            category_id=self.category_id,
        )
        return self.filtered_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update(
            {
                "page_title": _("Restaurants"),
                "search_q": self.q,
                "active_city": self.city,
                "active_category": self.category_id,
                "featured_cities": [
                    (code, label) for code, label in Restaurant.City.choices
                    if code in FEATURED_CITY_CODES
                ],
                "city_choices": get_all_city_choices(),
                "filter_categories": get_filter_categories(),
                "top_rated": get_top_rated_restaurants(limit=4),
                "restaurant_count": self.filtered_queryset.count(),
                "map_restaurant_count": get_map_restaurants(self.filtered_queryset).count(),
                "wishlist_ids": self._wishlist_ids(user),
                "map_restaurants": self._map_markers(),
                "map_i18n": {
                    "view": _("View"),
                    "viewRestaurant": _("View Restaurant"),
                },
            }
        )
        return context

    def _wishlist_ids(self, user) -> set[int]:
        if not user.is_authenticated or user.is_owner_role:
            return set()
        return set(
            Wishlist.objects.filter(user=user).values_list("restaurant_id", flat=True)
        )

    def _localized_name(self, restaurant) -> str:
        if translation.get_language() == "ar":
            return restaurant.name_ar or restaurant.name_en
        return restaurant.name_en or restaurant.name_ar

    def _map_markers(self) -> list[dict]:
        qs = get_map_restaurants(self.filtered_queryset)
        markers = []
        for r in qs:
            if r.latitude is None or r.longitude is None:
                continue
            markers.append(
                {
                    "id": r.pk,
                    "name": self._localized_name(r),
                    "lat": float(r.latitude),
                    "lng": float(r.longitude),
                    "url": reverse("restaurants:detail", args=[r.pk]),
                }
            )
        return markers


class RestaurantDetailView(DetailView):
    """Single restaurant profile with menu and reviews tabs."""

    template_name = "restaurants/detail.html"
    context_object_name = "restaurant"

    def get_object(self):
        return get_public_restaurant_detail(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.object
        user = self.request.user
        visible_reviews = restaurant.reviews.filter(is_visible=True)
        stats = visible_reviews.aggregate(
            avg=Avg("rating"),
            count=Count("id"),
        )
        active_tab = self.request.GET.get("tab", "menu")
        if active_tab not in ("menu", "reviews"):
            active_tab = "menu"

        user_review = None
        review_form = ReviewForm()
        draft = self.request.session.pop("review_form_post", None)
        if draft and draft.get("restaurant_pk") == restaurant.pk:
            review_form = ReviewForm(
                initial={
                    "rating": draft.get("rating") or 0,
                    "comment": draft.get("comment", ""),
                },
            )
        if user.is_authenticated and not user.is_owner_role:
            user_review = visible_reviews.filter(user=user).first()
            if user_review and not draft:
                review_form = ReviewForm(instance=user_review)
            elif user_review and draft:
                review_form = ReviewForm(
                    initial={
                        "rating": draft.get("rating") or user_review.rating,
                        "comment": draft.get("comment", user_review.comment),
                    },
                )

        context.update(
            {
                "page_title": restaurant.name_en,
                "active_tab": active_tab,
                "is_open_now": is_open_now(restaurant),
                "avg_rating": round(stats["avg"], 1) if stats["avg"] else None,
                "review_count": stats["count"] or 0,
                "rating_breakdown": get_rating_breakdown(restaurant),
                "reviews": visible_reviews,
                "review_form": review_form,
                "user_review": user_review,
                "in_wishlist": self._in_wishlist(user, restaurant),
                "menu_categories": restaurant.categories.all(),
            }
        )
        return context

    def _in_wishlist(self, user, restaurant) -> bool:
        if not user.is_authenticated or user.is_owner_role:
            return False
        return Wishlist.objects.filter(user=user, restaurant=restaurant).exists()


class WishlistToggleView(LoginRequiredMixin, View):
    """Add or remove a restaurant from the user's wishlist."""

    def post(self, request, pk):
        if request.user.is_owner_role:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {"success": False, "message": str(_("Owners cannot use wishlist."))},
                    status=403,
                )
            messages.error(request, _("Owners cannot use wishlist."))
            return redirect("restaurants:list")

        restaurant = get_object_or_404(
            Restaurant,
            pk=pk,
            status=Restaurant.Status.ACTIVE,
        )
        entry = Wishlist.objects.filter(user=request.user, restaurant=restaurant)
        added = False
        if entry.exists():
            entry.delete()
            message = str(_("Removed from wishlist"))
        else:
            Wishlist.objects.create(user=request.user, restaurant=restaurant)
            added = True
            message = str(_("Added to wishlist"))

        next_url = request.POST.get("next") or reverse("restaurants:list")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "added": added, "message": message})

        messages.success(request, message)
        return redirect(next_url)


class ReviewSubmitView(LoginRequiredMixin, View):
    """Create or update the current user's review on a restaurant."""

    def get_login_url(self):
        pk = self.kwargs["pk"]
        next_url = f"{reverse('restaurants:detail', args=[pk])}?tab=reviews"
        return f"{settings.LOGIN_URL}?{urlencode({'next': next_url})}"

    def get(self, request, pk):
        return redirect(f"{reverse('restaurants:detail', args=[pk])}?tab=reviews")

    def post(self, request, pk):
        if request.user.is_owner_role:
            messages.error(request, _("Owners cannot submit reviews."))
            return redirect("restaurants:detail", pk=pk)

        restaurant = get_object_or_404(
            Restaurant,
            pk=pk,
            status=Restaurant.Status.ACTIVE,
        )
        existing = Review.objects.filter(user=request.user, restaurant=restaurant).first()
        form = ReviewForm(request.POST, instance=existing)
        tab = "reviews"

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.is_visible = True
            review.save()
            if existing:
                messages.success(request, _("Your review has been updated."))
            else:
                messages.success(request, _("Thank you for your review!"))
            return redirect(f"{reverse('restaurants:detail', args=[pk])}?tab={tab}")

        request.session["review_form_post"] = {
            "restaurant_pk": pk,
            "rating": request.POST.get("rating", ""),
            "comment": request.POST.get("comment", ""),
        }
        for field_errors in form.errors.values():
            for err in field_errors:
                messages.error(request, err)
        return redirect(f"{reverse('restaurants:detail', args=[pk])}?tab={tab}")
