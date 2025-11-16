from typing import Any

from rest_framework import serializers

from apps.resume.models import ResumeModel, ResumeTemplateModel
from apps.resume.serializers.resume_section_serializer import (
    CourseGetSerializer,
    EducationGetSerializer,
    LanguageGetSerializer,
    LinkGetSerializer,
    ProjectGetSerializer,
    SkillGetSerializer,
    WorkExperienceGetSerializer,
)
from apps.users.models import UserModel


class ResumeTemplateNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeTemplateModel
        fields = ["id", "name"]


class CreateResumeSerializer(serializers.ModelSerializer):

    template = ResumeTemplateNestedSerializer(read_only=True)

    template_id = serializers.PrimaryKeyRelatedField(
        queryset=ResumeTemplateModel.objects.all(),
        source="template",
        write_only=True,
    )

    class Meta:
        model = ResumeModel
        fields = [
            "id",
            "resume_name",
            "job_title",
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "city",
            "summary",
            "template",
            "template_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data: dict[str, Any]):
        owner: UserModel = self.context["user"]

        return ResumeModel.objects.create(**validated_data, owner=owner)


class GetResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeModel
        fields = [
            "id",
            "resume_name",
            "job_title",
            "template",
            "created_at",
            "updated_at",
        ]


class GetResumeDetailSerializer(serializers.ModelSerializer):
    template = ResumeTemplateNestedSerializer(read_only=True)
    work_experience = WorkExperienceGetSerializer(many=True, read_only=True)
    projects = ProjectGetSerializer(many=True, read_only=True)
    education = EducationGetSerializer(many=True, read_only=True)
    links = LinkGetSerializer(many=True, read_only=True)
    skills = SkillGetSerializer(many=True, read_only=True)
    courses = CourseGetSerializer(many=True, read_only=True)
    languages = LanguageGetSerializer(many=True, read_only=True)

    class Meta:
        model = ResumeModel
        fields = [
            "id",
            "resume_name",
            "job_title",
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "city",
            "summary",
            "template",
            "work_experience",
            "projects",
            "education",
            "links",
            "skills",
            "courses",
            "languages",
            "created_at",
            "updated_at",
        ]


class UpdateResumeSerializer(serializers.ModelSerializer):
    template = ResumeTemplateNestedSerializer(read_only=True)

    class Meta:
        model = ResumeModel
        fields = [
            "id",
            "resume_name",
            "job_title",
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "city",
            "summary",
            "template",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "template", "created_at", "updated_at"]
