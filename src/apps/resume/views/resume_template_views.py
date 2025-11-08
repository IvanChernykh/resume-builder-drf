from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.resume.serializers.resume_template_serializer import ResumeTemplateSerializer
from apps.resume.services.resume_template_services import get_all_resume_templates
from utils.constants.drf_spectacular import AUTH_API_HEADER


@extend_schema(
    methods=["GET"],
    responses={200: ResumeTemplateSerializer},
    parameters=[AUTH_API_HEADER],
)
@api_view(["GET"])
def resume_template_view(request: Request):
    if request.method == "GET":
        return get_all_resume_templates(request)
