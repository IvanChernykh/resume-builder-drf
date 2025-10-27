from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.views import login, logout, register

app_name = "apps.authentication"

urlpatterns = [
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]
