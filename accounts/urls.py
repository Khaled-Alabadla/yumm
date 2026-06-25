"""URL patterns for the accounts app.

Mounted at /accounts/ from the root URLconf.

    /accounts/register/    sign up
    /accounts/login/       sign in  (also the target of settings.LOGIN_URL)
    /accounts/logout/      sign out
    /accounts/profile/     view / edit own profile
    /accounts/demo-login/  quick demo access — POST only, DEBUG mode only
"""

from django.urls import path

from .views import DemoLoginView, LoginView, LogoutView, ProfileView, RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/",   RegisterView.as_view(),  name="register"),
    path("login/",      LoginView.as_view(),      name="login"),
    path("logout/",     LogoutView.as_view(),     name="logout"),
    path("profile/",    ProfileView.as_view(),    name="profile"),
    path("demo-login/", DemoLoginView.as_view(),  name="demo-login"),
]
