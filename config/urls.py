"""Root URL configuration for the Yumm backend."""

from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views

import accounts

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', accounts.views.index, name='index'),
    # POST /i18n/set-language/  { language: "ar" | "en" }
    # LocaleMiddleware reads the resulting session/cookie on every request.
    # Templates use {% url 'set_language' %} to let users switch language.
    path("i18n/", include("django.conf.urls.i18n")),

    # Accounts — authentication and user profile
<<<<<<< Updated upstream
    path("accounts/", include("accounts.urls", namespace="accounts")),   
=======
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path('', views.index, name='index'),    path('about/',   views.about,   name='about'),
>>>>>>> Stashed changes
]
