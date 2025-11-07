from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.resume.services.resume_services import (
    create_resume,
    delete_resume,
    get_all_user_resumes,
    get_resume,
    update_resume,
)


@api_view(["Get", "POST"])
def resume_view(request: Request):
    if request.method == "GET":
        return get_all_user_resumes(request)

    if request.method == "POST":
        return create_resume(request)


@api_view(["GET", "PUT", "DELETE"])
def resume_detail_view(request: Request, resume_id: str):
    if request.method == "GET":
        return get_resume(request, resume_id)

    if request.method == "PUT":
        return update_resume(request, resume_id)

    if request.method == "DELETE":
        return delete_resume(request, resume_id)
