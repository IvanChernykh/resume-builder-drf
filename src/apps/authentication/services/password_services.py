import os
from typing import cast

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from apps.authentication.serializers import ChangePasswordSerializer
from apps.users.models import UserModel


def check_user_password(password: str | None, encoded: str) -> bool:
    return check_password(password, encoded)


def send_password_reset_email(user: UserModel, token: str) -> Response:
    reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password/?token={token}"
    message = f"Reset your password:\n{reset_url}"

    try:
        send_mail(
            subject="Password reset",
            message=message,
            recipient_list=[user.email],
            from_email="noreply@resumebuilder.com",
        )
        return Response({"message": "Password reset email has been sent"}, status=200)
    except Exception as e:
        print("Mail error:", e)
        return Response({"message": "Error"}, status=500)


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
