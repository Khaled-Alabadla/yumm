"""URL patterns for the restaurants app."""

from django.urls import path

from . import public_views, views

app_name = "restaurants"

urlpatterns = [
    path("restaurants/", public_views.RestaurantListView.as_view(), name="list"),
    path(
        "restaurants/<int:pk>/",
        public_views.RestaurantDetailView.as_view(),
        name="detail",
    ),
    path(
        "restaurants/<int:pk>/wishlist/",
        public_views.WishlistToggleView.as_view(),
        name="wishlist-toggle",
    ),
    path(
        "restaurants/<int:pk>/review/",
        public_views.ReviewSubmitView.as_view(),
        name="review-submit",
    ),
    path("dashboard/", views.DashboardOverviewView.as_view(), name="dashboard"),
    path(
        "dashboard/info/",
        views.DashboardInfoView.as_view(),
        name="dashboard-info",
    ),
    path(
        "dashboard/menu/",
        views.DashboardMenuView.as_view(),
        name="dashboard-menu",
    ),
    path(
        "dashboard/menu/add/",
        views.MenuItemCreateView.as_view(),
        name="dashboard-menu-add",
    ),
    path(
        "dashboard/menu/<int:pk>/edit/",
        views.MenuItemUpdateView.as_view(),
        name="dashboard-menu-edit",
    ),
    path(
        "dashboard/menu/<int:pk>/delete/",
        views.MenuItemDeleteView.as_view(),
        name="dashboard-menu-delete",
    ),
    path(
        "dashboard/reviews/",
        views.DashboardReviewsView.as_view(),
        name="dashboard-reviews",
    ),
    path(
        "dashboard/reviews/<int:pk>/reply/",
        views.ReviewReplyView.as_view(),
        name="dashboard-review-reply",
    ),
]
