from rest_framework import serializers

from apps.resume.models import ResumeModel
from apps.users.models import UserModel


class CreateResumeSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        owner: UserModel = self.context["request"].user
        resume = ResumeModel.objects.create(**validated_data, owner=owner)

        return resume
