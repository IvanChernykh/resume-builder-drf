import pytest

from apps.users.models import UserModel
from django.contrib.auth.hashers import make_password


@pytest.fixture
def user_1():
    return UserModel.objects.create(
        name="Johnny Silverhand",
        username="silverhand",
        email="joknny@mail.com",
        password=make_password("secret123"),
    )


@pytest.fixture
def user_2():
    return UserModel.objects.create(
        name="Shrek",
        username="swampguy",
        email="shrek@mail.com",
        password=make_password("getouttamyswamp"),
    )
