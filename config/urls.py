"""Root URL configuration for the Yumm backend."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from accounts import views


urlpatterns = [
    path("admin/", admin.site.urls),

    # POST /i18n/set-language/  { language: "ar" | "en" }
    path("i18n/", include("django.conf.urls.i18n")),

    # Accounts — authentication and user profile
    path("accounts/", include("accounts.urls", namespace="accounts")),

    # Restaurant owner dashboard
    path("", include("restaurants.urls", namespace="restaurants")),

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('ai/', include("ai_bot.urls", namespace="ai_bot")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
