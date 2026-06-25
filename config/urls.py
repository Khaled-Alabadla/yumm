"""Root URL configuration for the Yumm backend."""

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
]
