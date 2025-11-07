from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.resume.services.resume_template_services import get_all_resume_templates


@api_view(["GET"])
def resume_template_view(request: Request):
    if request.method == "GET":
        return get_all_resume_templates(request)
