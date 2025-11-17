import hashlib
import os

from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from apps.users.models import UserModel
from config.settings.jwt import JWT_REFRESH_TTL_SECONDS
from config.settings.redis import REDIS_JWT
from config.settings.settings import DEBUG
from libs.jwt_auth.token import JwtTokenPair, generate_jwt_pair


def get_redis_jwt_name(user: UserModel, token="") -> str:
    token_hash = hashlib.sha256(token.encode()).hexdigest()[:16]
    return f"{str(user.id)}_{token_hash}"


def get_tokens_for_user(user: UserModel) -> JwtTokenPair:
    return generate_jwt_pair({"sub": str(user.id)})


def set_refresh_token_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=not DEBUG,
        samesite="None",
        max_age=JWT_REFRESH_TTL_SECONDS,
    )


def get_token_pair_response(user: UserModel) -> Response:
    tokens = get_tokens_for_user(user)
    response = Response({"access_token": tokens["access"]}, status=status.HTTP_200_OK)

    REDIS_JWT.set(
        name=get_redis_jwt_name(user, tokens["refresh"]),
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


def send_verification_email(user: UserModel, token: str) -> Response:
    verify_url = f"{os.getenv('FRONTEND_URL')}/verify-email/?token={token}"

    message = f"""
    Hello, {user.username}!
    Please confirm your email address by clicking the link below:
    {verify_url}
    """

    try:
        send_mail(
            subject="Email confirmation",
            message=message,
            recipient_list=[user.email],
            from_email="noreply@resumebuilder.com",
        )
        return Response(
            {"message": "Verification email has been sent to your email adress"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        print(f"ERROR DUDE: {e}")

        return Response(
            {"message": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
