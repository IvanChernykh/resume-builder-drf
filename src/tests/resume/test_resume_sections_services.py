from typing import cast

import pytest
from django.http import Http404
from rest_framework import status

from apps.resume.models import (
    EducationModel,
    LinkModel,
    ProjectModel,
    SkillModel,
    WorkExperienceModel,
)
from apps.resume.services.resume_section_services import (
    create_resume_sections,
    delete_resume_sections,
    update_resume_sections,
)


# ---------- create sections ----------
@pytest.mark.django_db
def test_create_resume_sections(
    resume_user_1,
    user_1,
    make_work_experience_resume_user_1,
    make_education_resume_user_1,
    make_skills_resume_user_1,
):
    work_exp: WorkExperienceModel = make_work_experience_resume_user_1()[0]
    educ: EducationModel = make_education_resume_user_1(3)[0]
    make_skills_resume_user_1()

    data = {
        "work_experience": [
            {
                "job_title": f"{work_exp.job_title}-test",
                "sort_order": work_exp.sort_order,
            }
        ],
        "education": [{"school": educ.school, "sort_order": educ.sort_order}],
    }

    response = create_resume_sections(user_1, data, resume_user_1.id)
    res_data = cast(dict, response.data)

    assert response.status_code == status.HTTP_201_CREATED

    assert WorkExperienceModel.objects.count() == 2
    assert EducationModel.objects.count() == 4
    assert SkillModel.objects.count() == 1

    assert res_data["resume_name"] == resume_user_1.resume_name

    assert len(res_data["education"]) == 4
    assert len(res_data["work_experience"]) == 2
    assert len(res_data["links"]) == 0
    assert len(res_data["skills"]) == 1
    assert len(res_data["projects"]) == 0
    assert len(res_data["languages"]) == 0
    assert len(res_data["courses"]) == 0


@pytest.mark.django_db
def test_create_sections_should_return_404(resume_user_1, user_2):
    data = {}
    with pytest.raises(Http404):
        create_resume_sections(user_2, data, resume_user_1.id)


# ---------- update sections ----------
@pytest.mark.django_db
def test_update_resume_section(resume_user_1, user_1, make_education_resume_user_1):
    educ: list[EducationModel] = make_education_resume_user_1(3)

    educ_updated_item = educ[0]

    data = {
        "education": [
            {
                "id": str(educ_updated_item.id),
                "school": educ_updated_item.school,
                "degree": "wabba jabba",
                "city": "vice city",
                "start_end_date": educ_updated_item.start_end_date,
                "description": educ_updated_item.description,
                "sort_order": educ_updated_item.sort_order,
            }
        ],
    }

    response = update_resume_sections(user_1, data, resume_user_1.id)
    res_data = cast(dict, response.data)

    found = next(
        (x for x in res_data["education"] if x["id"] == str(educ_updated_item.id)), None
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(res_data["education"], list)
    assert found is not None
    assert found["city"] == "vice city"
    assert found["degree"] == "wabba jabba"
    assert found["school"] == educ_updated_item.school


@pytest.mark.django_db
def test_update_sections_should_return_404(resume_user_1, user_2):
    data = {}
    with pytest.raises(Http404):
        update_resume_sections(user_2, data, resume_user_1.id)


# ---------- delete sections ----------
@pytest.mark.django_db
def test_delete_resume_sections(
    resume_user_1,
    user_1,
    make_work_experience_resume_user_1,
    make_projects_resume_user_1,
    make_education_resume_user_1,
    make_skills_resume_user_1,
    make_links_resume_user_1,
    make_languages_resume_user_1,
    make_courses_resume_user_1,
):
    work_exp: list[WorkExperienceModel] = make_work_experience_resume_user_1(3)
    projects: list[ProjectModel] = make_projects_resume_user_1(3)
    educ: list[EducationModel] = make_education_resume_user_1(3)
    make_links_resume_user_1(3)
    make_skills_resume_user_1(3)
    make_languages_resume_user_1(3)
    make_courses_resume_user_1(3)

    data = {
        "work_experience": [work_exp[0].id],
        "projects": [projects[1].id],
        "education": [item.id for item in educ],
    }

    response = delete_resume_sections(user_1, data, resume_user_1.id)
    res_data = cast(dict, response.data)

    assert len(res_data["work_experience"]) == 2
    assert len(res_data["projects"]) == 2
    assert len(res_data["education"]) == 0
    assert len(res_data["links"]) == 3
    assert len(res_data["skills"]) == 3
    assert len(res_data["languages"]) == 3
    assert len(res_data["courses"]) == 3

    assert response.status_code == status.HTTP_200_OK

    assert WorkExperienceModel.objects.count() == 2
    assert ProjectModel.objects.count() == 2
    assert EducationModel.objects.count() == 0
    assert LinkModel.objects.count() == 3


@pytest.mark.django_db
def test_delete_sections_should_return_404(resume_user_1, user_2):
    data = {}
    with pytest.raises(Http404):
        delete_resume_sections(user_2, data, resume_user_1.id)
