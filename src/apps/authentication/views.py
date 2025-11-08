from typing import cast

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import EmailConfirmationTokenModel
from apps.authentication.serializers import LoginSerializer, RegisterSerializer
from apps.authentication.services import (
    authenticate_user,
    get_redis_jwt_name,
    get_token_pair_response,
    send_verification_email,
)
from apps.users.models import UserModel
from config.settings.redis import REDIS_JWT
from libs.jwt_auth.token import validate_jwt_token
from utils.constants.drf_spectacular import (
    ACCESS_TOKEN_API_RESPONSE,
    AUTH_API_HEADER,
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
)
@api_view(["POST"])
@authentication_classes([])
def refresh_token_view(request: Request):
    refresh_token = request.COOKIES.get("refresh_token")

    validated = validate_jwt_token(refresh_token, is_access_token=False)

    if validated:
        user = UserModel.objects.get(pk=validated["sub"])

        if user and REDIS_JWT.get(get_redis_jwt_name(user)):
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

    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token:
        REDIS_JWT.delete(get_redis_jwt_name(request.user, refresh_token))
        response.delete_cookie("refresh_token")

    return response


@extend_schema(
    methods=["POST"],
    responses={200: MESSAGE_SUCCESS_API_RESPONSE},
    parameters=[AUTH_API_HEADER],
)
@api_view(["POST"])
def send_verification_email_view(request: Request):
    user = request.user

    EmailConfirmationTokenModel.objects.filter(user=user).delete()

    new_token = EmailConfirmationTokenModel.objects.create(user=user)

    return send_verification_email(user, str(new_token.id))


@extend_schema(
    methods=["GET"],
    responses={200: MESSAGE_SUCCESS_API_RESPONSE},
    parameters=[AUTH_API_HEADER],
)
@api_view(["GET"])
def confirm_email_view(request: Request, token: str):
    user: UserModel = request.user

    try:
        confirmation_token = EmailConfirmationTokenModel.objects.select_related(
            "user"
        ).get(pk=token)
    except EmailConfirmationTokenModel.DoesNotExist:
        return Response(
            {"message": "token not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if confirmation_token.is_expired or not confirmation_token.belongs_to_user(user):
        return Response(
            {"message": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )

    user.email_verified = True
    user.save(update_fields=["email_verified"])

    confirmation_token.delete()

    return Response(
        {"message": "Your email has been verified"}, status=status.HTTP_200_OK
    )
