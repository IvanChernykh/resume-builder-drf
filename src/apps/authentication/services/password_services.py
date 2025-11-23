from typing import cast

from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.response import Response

from apps.authentication.serializers import ChangePasswordSerializer
from apps.users.models import UserModel


def check_user_password(password: str | None, encoded: str) -> bool:
    return check_password(password, encoded)


def change_password(data: dict[str, str], user: UserModel) -> Response:
    serializer = ChangePasswordSerializer(data=data)

    if serializer.is_valid():
        data = cast(dict, serializer.validated_data)

        if not check_user_password(data["old_password"], user.password):
            return Response(
                {"message": ["Incorrect old password"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.password = make_password(data["new_password"])
        user.save(update_fields=["password"])

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
