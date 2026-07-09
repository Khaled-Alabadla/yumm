"""URL patterns for the accounts app.

Mounted at /accounts/ from the root URLconf.

    /accounts/register/                          sign up
    /accounts/login/                             sign in
    /accounts/logout/                            sign out
    /accounts/profile/                           view / edit own profile
    /accounts/pending/                           owner awaiting approval
    /accounts/check-email/                       user: confirm email notice
    /accounts/verify-email/<uidb64>/<token>/     activate user account
    /accounts/demo-login/                        quick demo access (DEBUG)
"""

from django.urls import path

from .views import (
    CheckEmailView,
    DemoLoginView,
    LoginView,
    LogoutView,
    PendingView,
    ProfileView,
    RegisterView,
    VerifyEmailView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("demo-login/", DemoLoginView.as_view(), name="demo-login"),
    path("pending/", PendingView.as_view(), name="pending"),
    path("check-email/", CheckEmailView.as_view(), name="check_email"),
    path(
        "verify-email/<uidb64>/<token>/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
]
