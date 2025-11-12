import pytest
from apps.resume.models import ResumeTemplateModel


@pytest.fixture
def template():
    return ResumeTemplateModel.objects.create(name="Default Template")
