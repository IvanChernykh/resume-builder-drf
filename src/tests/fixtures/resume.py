import pytest
from apps.resume.models import ResumeModel, ResumeTemplateModel


@pytest.fixture
def resume_template():
    return ResumeTemplateModel.objects.create(name="Default Template")


@pytest.fixture
def resume_user_1(user_1, resume_template):
    return ResumeModel.objects.create(
        resume_name="Test Resume 1",
        job_title="CEO of Unemployment",
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        phone="123123123",
        country="UA",
        city="Kyiv",
        summary="Unexperienced specialist...",
        template=resume_template,
        owner=user_1,
    )


@pytest.fixture
def resume_user_2(user_2, resume_template):
    return ResumeModel.objects.create(
        resume_name="Test Resume 2",
        job_title="developer",
        first_name="mark",
        last_name="ronson",
        email="mark@example.com",
        phone="424242",
        country="UA",
        city="Kyiv",
        summary="lorem ipsum dolor sit amet",
        template=resume_template,
        owner=user_2,
    )
