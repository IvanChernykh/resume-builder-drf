from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response

from apps.users.models import UserModel
from config.settings.jwt import JWT_REFRESH_TTL_SECONDS
from config.settings.redis import REDIS_JWT
from libs.jwt_auth.token import JwtTokenPair, generate_jwt_pair


def get_redis_jwt_name(user: UserModel) -> str:
    # TODO: change name, cause user can have only one active session right now
    return str(user.id)


def get_tokens_for_user(user: UserModel) -> JwtTokenPair:
    return generate_jwt_pair({"sub": str(user.id)})


def set_refresh_token_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=False,  # TODO: should be True if isProd
        samesite="None",
        max_age=JWT_REFRESH_TTL_SECONDS,
    )


def get_token_pair_response(user: UserModel) -> Response:
    tokens = get_tokens_for_user(user)
    response = Response({"access_token": tokens["access"]}, status=status.HTTP_200_OK)

    REDIS_JWT.set(
        name=get_redis_jwt_name(user),
        value=tokens["refresh"],
        ex=JWT_REFRESH_TTL_SECONDS,
    )

    set_refresh_token_cookie(response, tokens["refresh"])

    return response


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
