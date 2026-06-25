"""Root URL configuration for the Yumm backend."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    # POST /i18n/set-language/  { language: "ar" | "en" }
    # LocaleMiddleware reads the resulting session/cookie on every request.
    # Templates use {% url 'set_language' %} to let users switch language.
    path("i18n/", include("django.conf.urls.i18n")),

    # Accounts — authentication and user profile
    path("accounts/", include("accounts.urls", namespace="accounts")),
]
