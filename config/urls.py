"""Root URL configuration for the Yumm backend."""

from django.conf.urls.i18n import set_language
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    # POST /i18n/set-language/  { language: "ar" | "en" }
    # LocaleMiddleware reads the resulting session key / cookie on
    # every subsequent request, so API clients call this once and then
    # pass the Accept-Language header or rely on the stored preference.
    path("i18n/", include("django.conf.urls.i18n")),
]
