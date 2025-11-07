from typing import Any

from rest_framework import serializers

from apps.resume.models import ResumeModel, ResumeTemplateModel
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
        owner: UserModel = self.context["request"].user

        return ResumeModel.objects.create(**validated_data, owner=owner)
