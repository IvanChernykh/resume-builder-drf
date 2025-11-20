import pytest
from django.contrib.auth.hashers import check_password
from rest_framework import status

from apps.authentication.services.password_services import change_password


@pytest.mark.django_db
def test_change_password(user_1):
    data = {"old_password": "secret123", "new_password": "shreks123"}
    response = change_password(data, user_1)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert check_password("shreks123", user_1.password)


@pytest.mark.django_db
def test_change_password_should_raise_password_too_short(user_1):
    data = {"old_password": "secret123", "new_password": "shreks"}
    response = change_password(data, user_1)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
