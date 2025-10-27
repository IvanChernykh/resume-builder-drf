from typing import cast

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers import LoginSerializer, RegisterSerializer
from apps.authentication.services import authenticate_user, get_tokens_for_user


@api_view(["POST"])
def register(request: Request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request: Request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        data = cast(dict[str, str], serializer.validated_data)
        user = authenticate_user(data)

        if user:
            tokens = get_tokens_for_user(user)
            response = Response(
                {"access_token": tokens["access"]}, status=status.HTTP_200_OK
            )

            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=False,  # TODO: should be True if isProd
                samesite="None",
                max_age=7 * 24 * 60 * 60,
            )

            return response
        else:
            return Response(
                {"message": "email or password does not match"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def logout(request: Request):
    return Response("Hello world")
    return Response("Hello world")
