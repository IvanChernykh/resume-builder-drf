from rest_framework import serializers

from apps.resume.models import ResumeTemplateModel


class ResumeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeTemplateModel
        fields = "__all__"
