from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.resume.models import ResumeTemplateModel
from apps.resume.serializers.resume_template_serializer import ResumeTemplateSerializer


def get_all_resume_templates(request: Request):
    resume_templates = ResumeTemplateModel.objects.all()
    serializer = ResumeTemplateSerializer(resume_templates, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
