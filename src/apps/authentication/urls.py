from django.urls import path

from apps.authentication.views import (
    change_password_view,
    confirm_email_view,
    get_csrf_token_view,
    login_view,
    logout_view,
    refresh_token_view,
    register_view,
    reset_password_confirm_view,
    reset_password_request_view,
    send_verification_email_view,
)

app_name = "apps.authentication"

urlpatterns = [
    path("csrf-token/", get_csrf_token_view, name="get_csrf_token"),
    path("refresh-token/", refresh_token_view, name="token_refresh"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path(
        "send-verification-email/",
        send_verification_email_view,
        name="send_verification_email",
    ),
    path("confirm-emal/<str:token>/", confirm_email_view, name="confirm_email"),
    path("password/change/", change_password_view, name="change_password"),
    path(
        "password/reset/request",
        reset_password_request_view,
        name="password_reset_request",
    ),
    path(
        "password/reset/confirm/<str:token>/",
        reset_password_confirm_view,
        name="password_reset_confirm",
    ),
]
