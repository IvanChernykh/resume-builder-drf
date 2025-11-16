from random import randint

import pytest

from apps.resume.models import (
    CourseModel,
    EducationModel,
    LanguageModel,
    LinkModel,
    ProjectModel,
    ResumeModel,
    ResumeTemplateModel,
    SkillModel,
    WorkExperienceModel,
)


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


# ---------- work experience ----------
@pytest.fixture
def make_work_experience_resume_user_1(resume_user_1):
    def _make_work_experience(count=1, **kwargs) -> list[WorkExperienceModel]:
        return [
            WorkExperienceModel.objects.create(
                job_title=kwargs.get("job_title", f"Job_{i}"),
                employer=kwargs.get("employer", f"Company_{i}"),
                city=kwargs.get("city", f"City_{i}"),
                start_end_date=kwargs.get("start_end_date", "Jan 1, 2000 - Present"),
                description=kwargs.get("description", "Lorem ipsum dolor sit amet"),
                sort_order=kwargs.get("sort_order", i),
                resume=resume_user_1,
            )
            for i in range(1, count + 1)
        ]

    return _make_work_experience


# ---------- skill ----------
@pytest.fixture
def make_skills_resume_user_1(resume_user_1):
    def _make_skills(count=1):
        return [
            SkillModel.objects.create(
                title=f"Skill_{i}",
                level=randint(1, 100),
                sort_order=i,
                resume=resume_user_1,
            )
            for i in range(1, count + 1)
        ]

    return _make_skills


# ---------- education ----------
@pytest.fixture
def make_education_resume_user_1(resume_user_1):
    def _make_education(count=1, **kwargs):
        return [
            EducationModel.objects.create(
                school=kwargs.get("school", f"School_{i}"),
                degree=kwargs.get("degree", f"Degree_{i}"),
                city=kwargs.get("city", f"City_{i}"),
                start_end_date=kwargs.get("start_end_date", "Jan 1, 2000 - Present"),
                description=kwargs.get("description", "Lorem ipsum dolor sit amet"),
                sort_order=kwargs.get("sort_order", i),
                resume=resume_user_1,
            )
            for i in range(1, count + 1)
        ]

    return _make_education


# ---------- project ----------
@pytest.fixture
def make_projects_resume_user_1(resume_user_1):
    def _make_projects(count=1, **kwargs):
        return [
            ProjectModel.objects.create(
                title=kwargs.get("title", f"Project_{i}"),
                link=kwargs.get("link", f"https://example.com/project_{i}"),
                link_to_repo=kwargs.get(
                    "link_to_repo", f"https://github.com/project_{i}"
                ),
                description=kwargs.get("description", "Lorem ipsum dolor sit amet"),
                sort_order=kwargs.get("sort_order", i),
                resume=resume_user_1,
            )
            for i in range(1, count + 1)
        ]

    return _make_projects


# ---------- course ----------
@pytest.fixture
def make_courses_resume_user_1(resume_user_1):
    def _make_courses(count=1, **kwargs):
        return [
            CourseModel.objects.create(
                course=kwargs.get("course", f"Course_{i}"),
                institution=kwargs.get("institution", f"Institution_{i}"),
                start_end_date=kwargs.get("start_end_date", "Jan 1, 2000 - Present"),
                sort_order=kwargs.get("sort_order", i),
                resume=resume_user_1,
            )
            for i in range(1, count + 1)
        ]

    return _make_courses


# ---------- link ----------
@pytest.fixture
def make_links_resume_user_1(resume_user_1):
    def _make_links(count=1, **kwargs):
        return [
            LinkModel.objects.create(
                title=kwargs.get("title", f"Link_{i}"),
                link=kwargs.get("link", f"https://example.com/link_{i}"),
                sort_order=kwargs.get("sort_order", i),
                resume=resume_user_1,
            )
            for i in range(1, count + 1)
        ]

    return _make_links


# ---------- language ----------
@pytest.fixture
def make_languages_resume_user_1(resume_user_1):
    def _make_languages(count=1, **kwargs):
        return [
            LanguageModel.objects.create(
                language=kwargs.get("language", f"Language_{i}"),
                level=kwargs.get("level", f"Level_{i}"),
                sort_order=kwargs.get("sort_order", i),
                resume=resume_user_1,
            )
            for i in range(1, count + 1)
        ]

    return _make_languages
