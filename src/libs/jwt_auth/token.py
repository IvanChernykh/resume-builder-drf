from datetime import datetime, timedelta, timezone
from typing import TypedDict

import jwt
from django.conf import settings

jwt_settings = {
    "algorithm": "HS256",
    "access_exp": timedelta(minutes=10),
    "refresh_exp": timedelta(days=7),
    "access_secret": "this_is_default_access_secret_dude",
    "refresh_secret": "this_is_default_refresh_secret_dude",
    **settings.JWT_SETTINGS,
}


class JwtPayload(TypedDict):
    sub: str | int


class JwtTokenPair(TypedDict):
    access: str
    refresh: str


def create_jwt_token(
    payload: JwtPayload,
    secret: str,
    exp: timedelta,
):
    jwt_payload: dict = {
        **payload,
        "exp": datetime.now(timezone.utc) + exp,
    }

    token = jwt.encode(jwt_payload, secret, algorithm=jwt_settings["algorithm"])

    return token


def generate_jwt_pair(payload: JwtPayload) -> JwtTokenPair:
    return {
        "access": create_jwt_token(
            payload, jwt_settings["access_secret"], jwt_settings["access_exp"]
        ),
        "refresh": create_jwt_token(
            payload, jwt_settings["refresh_secret"], jwt_settings["refresh_exp"]
        ),
    }


def validate_jwt_token(token: str, is_access_token):
    try:
        secret = (
            jwt_settings["access_secret"]
            if is_access_token
            else jwt_settings["refresh_secret"]
        )

        decoded: dict = jwt.decode(
            token,
            secret,
            algorithms=[jwt_settings["algorithm"]],
            options={"verify_exp": True},
        )
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token exired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"invalit token: {e}")
        return None
