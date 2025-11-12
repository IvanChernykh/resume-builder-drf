from typing import cast

import pytest

from apps.resume.models import ResumeModel
from apps.resume.services.resume_services import create_resume


@pytest.mark.django_db
def test_create_resume_success(user, template):
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
        "template_id": template.id,
    }

    response = create_resume(user=user, data=data)
    data = cast(dict, response.data)

    assert response.status_code == 201
    assert data["resume_name"] == data["resume_name"]
    assert data["job_title"] == data["job_title"]
    assert data["template"]["id"] == str(template.id)

    resume = ResumeModel.objects.get(id=data["id"])

    assert resume.owner == user
    assert resume.template == template
