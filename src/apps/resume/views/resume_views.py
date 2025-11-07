from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.resume.services.resume_services import create_resume


@api_view(["POST"])
def resume_view(request: Request):
    if request.method == "POST":
        return create_resume(request)
