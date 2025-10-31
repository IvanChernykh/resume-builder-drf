from django.urls import path

from apps.authentication.views import (
    confirm_email_view,
    login_view,
    logout_view,
    refresh_token_view,
    register_view,
    send_verification_email_view,
)

app_name = "apps.authentication"

urlpatterns = [
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
]
