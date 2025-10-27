from django.urls import path

from apps.authentication.views import (
    login_view,
    logout_view,
    refresh_token_view,
    register_view,
)

app_name = "apps.authentication"

urlpatterns = [
    path("refresh-token/", refresh_token_view, name="token_refresh"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
