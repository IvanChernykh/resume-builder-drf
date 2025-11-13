from typing import cast
import pytest

from apps.resume.models import ResumeTemplateModel
from apps.resume.services.resume_template_services import get_all_resume_templates


@pytest.mark.django_db
def test_get_all_resume_templates(resume_template):
    ResumeTemplateModel.objects.create(name="not a default template")

    response = get_all_resume_templates()

    data = cast(dict, response.data)

    assert isinstance(data, list)
    assert len(data) == 2

    names = [item["name"] for item in data]

    assert "not a default template" in names
    assert "Default Template" in names
