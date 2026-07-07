"""Django settings for the Yumm backend project."""

import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-replace-this-key-before-production",
)

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    # i18n helper — provides the built-in set_language redirect view
    "django.conf.urls.i18n",
    # Third-party
    "rest_framework",
    "corsheaders",
    # Local apps
    "accounts.apps.AccountsConfig",
    "restaurants.apps.RestaurantsConfig",
    "reviews.apps.ReviewsConfig",
    "ai_bot.apps.AiBotConfig",
]

# LocaleMiddleware must come after SessionMiddleware and before CommonMiddleware
# so it can read the session/cookie language preference on every request.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "accounts.middleware.OwnerDashboardRedirectMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.CustomErrorPageMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.navbar",
                "accounts.context_processors.wishlist",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE", "yumm_db"),
        "USER": os.getenv("MYSQL_USER", "root"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", "root"),
        "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "OPTIONS": {
            # utf8mb4 is required for Arabic text and emoji storage
            "charset": "utf8mb4",
            # Keep session time zone in UTC; avoids some MySQL datetime issues.
            "init_command": (
                "SET sql_mode='STRICT_TRANS_TABLES', time_zone='+00:00'"
            ),
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


# ---------------------------------------------------------------------------
# Internationalization (i18n)
# ---------------------------------------------------------------------------

# Active language set per-request by LocaleMiddleware via:
#   1. URL prefix  (if using i18n_patterns in urls.py)
#   2. Session key LANGUAGE_SESSION_KEY
#   3. Cookie      LANGUAGE_COOKIE_NAME
#   4. Accept-Language HTTP header  ← primary mechanism for REST API clients
#   5. LANGUAGE_CODE fallback below
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("ar", _("Arabic")),
]

USE_I18N = True

# Tell Django where to find the project-level .po / .mo translation files.
# Per-app translations live inside each app's own locale/ folder (auto-found).
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

TIME_ZONE = "Asia/Jerusalem"

USE_TZ = True


# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"


# ---------------------------------------------------------------------------
# Jazzmin — Yumm admin panel theme
# ---------------------------------------------------------------------------

JAZZMIN_SETTINGS = {
    # Branding — matches the public Yumm site
    "site_title": "Yumm Admin",
    "site_header": "Yumm",
    "site_brand": "Yumm",
    "site_logo": "img/yumm-logo.svg",
    "site_icon": "img/yumm-logo.svg",
    "login_logo": "img/yumm-logo.svg",
    "site_logo_classes": "yumm-brand-logo",
    "welcome_sign": _("Welcome back — Yumm Admin"),
    "copyright": "Yumm Palestine",

    # Custom assets — full Yumm styling (CSS + light-mode / RTL JS)
    "custom_css": "admin/css/yumm_admin.css",
    "custom_js": "admin/js/yumm_admin.js",

    # Single search bar in navbar
    "search_model": ["restaurants.Restaurant"],

    # Top navbar — minimal; sidebar handles full navigation
    "topmenu_links": [
        {
            "name": _("Dashboard"),
            "url": "admin:index",
            "permissions": ["auth.view_user"],
        },
        {
            "name": _("Restaurants"),
            "url": "admin:restaurants_restaurant_changelist",
            "permissions": ["restaurants.view_restaurant"],
        },
        {
            "name": _("Reviews"),
            "url": "admin:reviews_review_changelist",
            "permissions": ["reviews.view_review"],
        },
    ],

    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["auth"],
    "hide_models": [],
    "order_with_respect_to": [
        "accounts",
        "restaurants",
        "reviews",
    ],

    # Model icons (Font Awesome 5)
    "icons": {
        "accounts": "fas fa-users-cog",
        "accounts.CustomUser": "fas fa-user",
        "accounts.ContactMessage": "fas fa-envelope",
        "restaurants": "fas fa-store",
        "restaurants.Restaurant": "fas fa-utensils",
        "restaurants.RestaurantCategory": "fas fa-list",
        "restaurants.RestaurantImage": "fas fa-images",
        "restaurants.Tag": "fas fa-tags",
        "restaurants.MenuCategory": "fas fa-book-open",
        "restaurants.MenuItem": "fas fa-hamburger",
        "reviews": "fas fa-comments",
        "reviews.Review": "fas fa-star",
        "reviews.ReviewImage": "fas fa-camera",
        "reviews.CommentReply": "fas fa-reply",
        "reviews.Wishlist": "fas fa-heart",
        "reviews.Notification": "fas fa-bell",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # UX
    "related_modal_active": False,
    "use_google_fonts_cdn": False,
    "show_ui_builder": False,
    "show_theme_chooser": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "accounts.customuser": "collapsible",
        "restaurants.restaurant": "horizontal_tabs",
    },

    # Bilingual language switcher (Arabic / English)
    "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "default",
    "default_theme_mode": "light",
    "navbar": "navbar-white navbar-light",
    "navbar_fixed": True,
    "footer_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_fixed": True,
    "sidebar_nav_flat_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_compact_style": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "accent": "accent-danger",
    "brand_colour": "navbar-white",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


# ---------------------------------------------------------------------------
# Authentication redirects
# ---------------------------------------------------------------------------

# Where LoginRequiredMixin and @login_required send unauthenticated users.
LOGIN_URL = "/accounts/login/"

# Where Django's LoginView redirects after a successful login when no
# ?next= parameter is present.
LOGIN_REDIRECT_URL = "/"

# Where Django's LogoutView redirects after logging out.
LOGOUT_REDIRECT_URL = "/accounts/login/"


# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}
