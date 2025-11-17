from rest_framework import authentication, exceptions
from rest_framework.request import Request

from apps.users.models import UserModel
from libs.jwt_auth.token import validate_jwt_token
from utils.constants.headers import HEADER_AUTHORIZATION


class JwtAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[UserModel, str]:
        access_token_header: str = request.headers.get(HEADER_AUTHORIZATION)

        if not access_token_header or not access_token_header.startswith("Bearer "):
            raise exceptions.AuthenticationFailed()

        try:
            token = access_token_header.split(" ", 1)[1]
        except IndexError:
            raise exceptions.AuthenticationFailed("oh no")

        validated = validate_jwt_token(token, is_access_token=True)

        if not validated:
            raise exceptions.AuthenticationFailed("Token invalid or exired")

        user = UserModel.objects.get(pk=validated["sub"])

        if not user:
            raise exceptions.AuthenticationFailed()

        return (user, token)
