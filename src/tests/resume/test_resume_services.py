from typing import cast

import pytest
from django.http import Http404
from rest_framework import status
from apps.resume.models import ResumeModel
from apps.resume.services.resume_services import (
    create_resume,
    delete_resume,
    update_resume,
)
from apps.users.models import UserModel


@pytest.mark.django_db
def test_create_resume(user_1, resume_template):
    data = {
        "resume_name": "asdasd",
        "job_title": "asd",
        "first_name": "Johnny",
        "last_name": "asdasd",
        "email": "john@example.com",
        "phone": "123123123",
        "country": "UA",
        "city": "Night city",
        "summary": "My summary",
        "template_id": resume_template.id,
    }

    response = create_resume(user=user_1, data=data)
    data = cast(dict, response.data)

    assert response.status_code == 201
    assert data["resume_name"] == data["resume_name"]
    assert data["job_title"] == data["job_title"]
    assert data["template"]["id"] == str(resume_template.id)

    resume = ResumeModel.objects.get(id=data["id"])

    assert resume.owner == user_1
    assert resume.template == resume_template


@pytest.mark.django_db
def test_update_resume(resume_user_1: ResumeModel, user_1: UserModel):
    data = {
        "resume_name": "Updated Resume Name",
        "job_title": "test job title",
        "first_name": "jimmy",
        "last_name": "page",
    }

    response = update_resume(data, user_1, resume_user_1.id)

    data = cast(dict, response.data)

    updated_resume = ResumeModel.objects.get(pk=resume_user_1.id)

    assert updated_resume.resume_name == "Updated Resume Name"

    assert data["resume_name"] == updated_resume.resume_name
    assert data["job_title"] == updated_resume.job_title

    assert data["first_name"] == "jimmy"
    assert data["last_name"] == "page"


@pytest.mark.django_db
def test_update_resume_should_raise_404(resume_user_1: ResumeModel, user_2: UserModel):
    data = {
        "resume_name": "Updated Resume Name",
    }

    with pytest.raises(Http404):
        update_resume(data, user_2, resume_user_1.id)


@pytest.mark.django_db
def test_delete_resume(resume_user_1, user_1):
    resume_id = resume_user_1.id
    response = delete_resume(user_1, resume_id)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not ResumeModel.objects.filter(id=resume_id).exists()


@pytest.mark.django_db
def test_delete_resume_should_raise_404(resume_user_1, user_2):
    with pytest.raises(Http404):
        delete_resume(user_2, resume_user_1.id)
