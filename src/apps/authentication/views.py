import secrets
from typing import cast

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from apps.authentication.serializers import (
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordConfirmSerializer,
    ResetPasswordRequestSerializer,
)
from apps.authentication.services import (
    authenticate_user,
    change_password,
    get_redis_jwt_name,
    get_token_pair_response,
    send_password_reset_email,
    send_verification_email,
)
from apps.users.models import UserModel
from config.settings.redis import REDIS_EMAIL_TOKEN, REDIS_JWT, REDIS_PW_RESET_TOEKN
from config.settings.settings import DEBUG
from libs.jwt_auth.token import validate_jwt_token
from libs.middleware.csrf_permission import DoubleSubmitCSRF
from utils.constants.cookies import COOKIE_CSRF_TOKEN, COOKIE_REFRESH_TOKEN
from utils.constants.drf_spectacular import (
    ACCESS_TOKEN_API_RESPONSE,
    AUTH_API_HEADER,
    CSRF_API_HEADER,
    MESSAGE_SUCCESS_API_RESPONSE,
)


@extend_schema(
    methods=["POST"],
    request=RegisterSerializer,
    responses={200: ACCESS_TOKEN_API_RESPONSE},
)
@api_view(["POST"])
@authentication_classes([])
def register_view(request: Request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = cast(UserModel, serializer.save())
        return get_token_pair_response(user)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=["POST"],
    request=LoginSerializer,
    responses={200: ACCESS_TOKEN_API_RESPONSE},
)
@api_view(["POST"])
@authentication_classes([])
def login_view(request: Request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        data = cast(dict[str, str], serializer.validated_data)

        user = authenticate_user(data)

        if user:
            return get_token_pair_response(user)
        else:
            return Response(
                {"message": "email or password does not match"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    methods=["POST"],
    responses={200: ACCESS_TOKEN_API_RESPONSE},
    parameters=[CSRF_API_HEADER],
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([DoubleSubmitCSRF])
def refresh_token_view(request: Request):
    refresh_token = request.COOKIES.get(COOKIE_REFRESH_TOKEN)

    validated = validate_jwt_token(refresh_token, is_access_token=False)

    if validated:
        user = UserModel.objects.get(pk=validated["sub"])

        if user and REDIS_JWT.get(get_redis_jwt_name(user, refresh_token)):
            return get_token_pair_response(user)

    return Response({"message": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=["POST"],
    responses={204: None},
    parameters=[AUTH_API_HEADER],
)
@api_view(["POST"])
def logout_view(request: Request):
    response = Response(status=status.HTTP_204_NO_CONTENT)

    refresh_token = request.COOKIES.get(COOKIE_REFRESH_TOKEN)

    if refresh_token:
        REDIS_JWT.delete(get_redis_jwt_name(request.user, refresh_token))
        response.delete_cookie(COOKIE_REFRESH_TOKEN)
        response.delete_cookie(COOKIE_CSRF_TOKEN)

    return response


EMAIL_VERIFICATION_TTL = 600
EMAIL_VERIFICATION_KEY = "email_verify:{}"


@extend_schema(
    methods=["POST"],
    responses={200: MESSAGE_SUCCESS_API_RESPONSE},
    parameters=[AUTH_API_HEADER],
)
@api_view(["POST"])
def send_verification_email_view(request: Request):
    user = request.user

    for key in REDIS_EMAIL_TOKEN.scan_iter(match="email_verify:*"):
        uid = REDIS_EMAIL_TOKEN.get(key)
        if str(uid) == str(user.id):
            REDIS_EMAIL_TOKEN.delete(key)

    token = secrets.token_urlsafe(32)

    redis_key = EMAIL_VERIFICATION_KEY.format(token)
    REDIS_EMAIL_TOKEN.setex(redis_key, EMAIL_VERIFICATION_TTL, user.id)

    return send_verification_email(user, token)


@extend_schema(
    methods=["GET"],
    responses={200: MESSAGE_SUCCESS_API_RESPONSE},
    parameters=[AUTH_API_HEADER],
)
@api_view(["GET"])
def confirm_email_view(request: Request, token: str):
    user: UserModel = request.user

    redis_key = EMAIL_VERIFICATION_KEY.format(token)

    stored_user_id = REDIS_EMAIL_TOKEN.get(redis_key)

    if stored_user_id is None:
        return Response(
            {"message": "token not found or expired"}, status=status.HTTP_404_NOT_FOUND
        )

    if str(user.id) != str(stored_user_id):
        return Response(
            {"message": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    user.email_verified = True
    user.save(update_fields=["email_verified"])

    REDIS_EMAIL_TOKEN.delete(redis_key)

    return Response(
        {"message": "Your email has been verified"}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_csrf_token_view(request: Request):
    token = secrets.token_urlsafe(32)

    response = Response({COOKIE_CSRF_TOKEN: token}, status=status.HTTP_200_OK)
    response.set_cookie(
        COOKIE_CSRF_TOKEN,
        token,
        httponly=True,
        secure=not DEBUG,
        samesite="Strict",
    )

    return response


@api_view(["POST"])
def change_password_view(request: Request):
    data = cast(dict, request.data)

    return change_password(data, request.user)


PW_RESET_TTL = 600
PW_RESET_KEY = "pw_reset:{}"


@api_view(["POST"])
def reset_password_request_view(request: Request):
    serializer = ResetPasswordRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = cast(dict, serializer.validated_data)["email"]

    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return Response({"message": "email has been sent"}, status=status.HTTP_200_OK)

    for key in REDIS_PW_RESET_TOEKN.scan_iter(match="pw_reset:*"):
        uid = REDIS_PW_RESET_TOEKN.get(key)
        if str(uid) == str(user.id):
            REDIS_PW_RESET_TOEKN.delete(key)

    token = secrets.token_urlsafe(32)

    redis_key = PW_RESET_KEY.format(token)
    REDIS_PW_RESET_TOEKN.setex(redis_key, PW_RESET_TTL, user.id)

    send_password_reset_email(user, token)

    return Response({"message": "email has been sent"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def reset_password_confirm_view(request: Request, token: str):
    serializer = ResetPasswordConfirmSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    new_password = cast(dict, serializer.validated_data)["new_password"]

    user_id = REDIS_PW_RESET_TOEKN.get(token)
    if not user_id:
        return Response({"message": "Invalid or expired token"}, status=400)

    try:
        user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    user.password = make_password(new_password)
    user.save(update_fields=["password"])

    REDIS_PW_RESET_TOEKN.delete(token)

    return Response({"message": "Password has been reset"}, status=200)
