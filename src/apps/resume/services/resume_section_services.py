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
