"""Restaurant-owner dashboard views."""

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView

from reviews.models import CommentReply, Review

from .forms import (
    MenuItemForm,
    RestaurantInfoForm,
    ReviewReplyForm,
    get_or_create_default_menu_category,
)
from .mixins import RestaurantOwnerMixin
from .models import MenuItem
from .utils import get_review_stats


class DashboardOverviewView(RestaurantOwnerMixin, TemplateView):
    """Overview tab — stats cards and recent reviews."""

    template_name = "restaurants/dashboard/overview.html"
    active_tab = "overview"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = get_review_stats(self.restaurant)
        context.update(stats)
        context["recent_reviews"] = (
            self.restaurant.reviews.filter(is_visible=True)
            .select_related("user")
            .order_by("-created_at")[:5]
        )
        return context


class DashboardInfoView(RestaurantOwnerMixin, TemplateView):
    """Restaurant Info tab — edit profile fields."""

    template_name = "restaurants/dashboard/info.html"
    active_tab = "info"

    def get_form(self):
        if self.request.method == "POST":
            return RestaurantInfoForm(self.request.POST, instance=self.restaurant)
        return RestaurantInfoForm(instance=self.restaurant)

    def get(self, request, *args, **kwargs):
        self.object = self.restaurant
        return self.render_to_response(self.get_context_data(form=self.get_form()))

    def post(self, request, *args, **kwargs):
        self.object = self.restaurant
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, _("Restaurant information saved."))
            return redirect("restaurants:dashboard-info")
        messages.error(
            request,
            _("Please correct the errors below."),
        )
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", self.get_form())
        return context


class DashboardMenuView(RestaurantOwnerMixin, TemplateView):
    """Menu tab — list items and modal add/edit forms."""

    template_name = "restaurants/dashboard/menu.html"
    active_tab = "menu"

    def get_context_data(self, **kwargs):
        return self.get_menu_page_context(**kwargs)


class MenuItemCreateView(RestaurantOwnerMixin, View):
    """POST — create a new menu item."""

    def post(self, request, *args, **kwargs):
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = self.restaurant
            item.category = get_or_create_default_menu_category(self.restaurant)
            item.is_available = True
            item.save()
            messages.success(request, _("Menu item added."))
            return redirect("restaurants:dashboard-menu")

        messages.error(request, _("Could not add menu item. Check the form."))
        context = self.get_menu_page_context(
            item_form=form,
            show_add_modal=True,
        )
        return render(request, "restaurants/dashboard/menu.html", context)


class MenuItemUpdateView(RestaurantOwnerMixin, View):
    """POST — update an existing menu item."""

    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(
            MenuItem,
            pk=pk,
            restaurant=self.restaurant,
        )
        form = MenuItemForm(
            request.POST,
            request.FILES,
            instance=item,
        )
        if form.is_valid():
            updated = form.save(commit=False)
            updated.is_available = True
            updated.save()
            messages.success(request, _("Menu item updated."))
            return redirect("restaurants:dashboard-menu")

        messages.error(request, _("Could not update menu item."))
        edit_forms = {
            menu_item.pk: MenuItemForm(instance=menu_item)
            for menu_item in self.restaurant.menu_items.all()
        }
        edit_forms[item.pk] = form
        context = self.get_menu_page_context(
            edit_forms=edit_forms,
            show_edit_modal=item.pk,
        )
        return render(request, "restaurants/dashboard/menu.html", context)


class MenuItemDeleteView(RestaurantOwnerMixin, View):
    """POST — remove a menu item (supports AJAX + SweetAlert flow)."""

    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(
            MenuItem,
            pk=pk,
            restaurant=self.restaurant,
        )
        item.delete()
        message = str(_("Menu item deleted."))

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": message})

        messages.success(request, message)
        return redirect("restaurants:dashboard-menu")


class DashboardReviewsView(RestaurantOwnerMixin, TemplateView):
    """Reviews tab — all customer reviews with reply inputs."""

    template_name = "restaurants/dashboard/reviews.html"
    active_tab = "reviews"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = (
            self.restaurant.reviews.filter(is_visible=True)
            .select_related("user")
            .prefetch_related("replies__user")
            .order_by("-created_at")
        )
        context["reviews"] = reviews
        context["reply_forms"] = {
            review.pk: ReviewReplyForm() for review in reviews
        }
        return context


class ReviewReplyView(RestaurantOwnerMixin, View):
    """POST — submit an owner reply to a review."""

    def post(self, request, pk, *args, **kwargs):
        review = get_object_or_404(
            Review,
            pk=pk,
            restaurant=self.restaurant,
        )
        form = ReviewReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.user = request.user
            reply.save()
            messages.success(request, _("Reply posted."))
        else:
            messages.error(request, _("Reply could not be posted."))
        return redirect("restaurants:dashboard-reviews")
