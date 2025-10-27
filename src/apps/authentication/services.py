from django.contrib.auth.hashers import check_password

from apps.users.models import UserModel
from libs.jwt_auth.token import JwtTokenPair, generate_jwt_pair


def get_tokens_for_user(user) -> JwtTokenPair:
    return generate_jwt_pair({"sub": user["id"]})


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
