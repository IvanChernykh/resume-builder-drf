from typing import cast

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers import LoginSerializer, RegisterSerializer
from apps.authentication.services import (
    authenticate_user,
    get_redis_jwt_name,
    get_token_pair_response,
)
from apps.users.models import UserModel
from config.settings.redis import REDIS_JWT
from libs.jwt_auth.token import validate_jwt_token


# TODO: token rotation
@api_view(["POST"])
@authentication_classes([])
def register_view(request: Request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = cast(UserModel, serializer.save())
        return get_token_pair_response(user)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["POST"])
def logout_view(request: Request):
    response = Response(status=status.HTTP_204_NO_CONTENT)
    print(REDIS_JWT.get(get_redis_jwt_name(request.user)))
    REDIS_JWT.delete(get_redis_jwt_name(request.user))
    response.delete_cookie("refresh_token")

    return response
