from typing import TypedDict

from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import UserModel


class JwtTokenPair(TypedDict):
    access: str
    refresh: str


def get_tokens_for_user(user) -> JwtTokenPair:
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def authenticate_user(data: dict[str, str]) -> UserModel | None:
    email = data.get("email")
    password = data.get("password")

    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return None

    if not check_password(password, user.password):
        return None

    return user
