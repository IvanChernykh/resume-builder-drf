from typing import Type, TypeVar, cast

from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apps.resume.models import (
    CourseModel,
    EducationModel,
    LanguageModel,
    LinkModel,
    ProjectModel,
    ResumeModel,
    SkillModel,
    WorkExperienceModel,
)
from apps.resume.serializers.resume_section_serializer import (
    CopySectionSerializer,
    CreateSectionsSerializer,
    DeleteSectionsSerializer,
    UpdateSectionsSerializer,
)
from apps.resume.serializers.resume_serializer import GetResumeDetailSerializer
from apps.users.models import UserModel

T = TypeVar("T", bound=models.Model)

section_mapping = {
    "work_experience": WorkExperienceModel,
    "education": EducationModel,
    "projects": ProjectModel,
    "skills": SkillModel,
    "courses": CourseModel,
    "links": LinkModel,
    "languages": LanguageModel,
}


# -------------------------------------------------------------------
# create sections
# -------------------------------------------------------------------
def create_entities(model: Type[T], resume, items: list[dict] | None):
    if not items:
        return
    objs = [model(resume=resume, **item) for item in items]
    model.objects.bulk_create(objs)


def create_resume_sections(
    user: UserModel, data: dict[str, list], resume_id: str
) -> Response:
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=user)

    serializer = CreateSectionsSerializer(data=data)

    if serializer.is_valid():
        validated_data = cast(dict[str, list[dict]], serializer.validated_data)

        for section_name, model in section_mapping.items():
            items = validated_data.get(section_name)
            create_entities(model, resume, items)

        get_serializer = GetResumeDetailSerializer(resume)

        return Response(data=get_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------
# update sections
# -------------------------------------------------------------------
def update_entities(model: Type[T], resume, items: list[dict] | None):
    if not items:
        return

    for item in items:
        obj_id = item.pop("id")
        fields = item
        model.objects.filter(pk=obj_id, resume=resume).update(**fields)


def update_resume_sections(
    user: UserModel, data: dict[str, list], resume_id: str
) -> Response:
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=user)

    serializer = UpdateSectionsSerializer(data=data)

    if serializer.is_valid():
        validated_data = cast(dict[str, list[dict]], serializer.validated_data)

        for section_name, model in section_mapping.items():
            items = validated_data.get(section_name)
            update_entities(model, resume, items)

        get_serializer = GetResumeDetailSerializer(resume)
        return Response(data=get_serializer.data, status=status.HTTP_200_OK)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------
# delete sections
# -------------------------------------------------------------------
def delete_resume_sections(
    user: UserModel, data: dict[str, list], resume_id: str
) -> Response:
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=user)

    serializer = DeleteSectionsSerializer(data=data)

    if serializer.is_valid():
        validated_data = cast(dict[str, list[str]], serializer.validated_data)

        for section_name, model in section_mapping.items():
            ids = validated_data.get(section_name)

            if not ids:
                continue

            model.objects.filter(pk__in=ids, resume=resume).delete()

        get_serializer = GetResumeDetailSerializer(resume)
        return Response(data=get_serializer.data, status=status.HTTP_200_OK)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------
# copy sections
# -------------------------------------------------------------------
def copy_section_entity(
    resume: ResumeModel, target_resume: ResumeModel, model: Type[T], id: str
):
    section_to_copy = get_object_or_404(model, pk=id, resume=resume)

    section_data = {
        field.name: getattr(section_to_copy, field.name)
        for field in model._meta.get_fields()
        if field.concrete and field.name not in ("id", "resume")
    }

    model.objects.create(resume=target_resume, **section_data)


def copy_resume_sections(user: UserModel, data: dict[str, list], resume_id: str):
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=user)
    serializer = CopySectionSerializer(data=data)

    if serializer.is_valid():
        validated_data = cast(dict[str, str], serializer.validated_data)

        target_resume = get_object_or_404(
            ResumeModel, pk=validated_data["target_resume"], owner=user
        )

        for section_name, model in section_mapping.items():
            id = validated_data.get(section_name)

            if not id:
                continue

            copy_section_entity(resume, target_resume, model, id)

        return Response(status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
