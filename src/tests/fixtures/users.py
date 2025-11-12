import pytest

from apps.users.models import UserModel


@pytest.fixture
def user():
    return UserModel.objects.create(
        name="Johnny Silverhand",
        username="silverhand",
        email="joknny@mail.com",
        password="secret123",
    )
