from typing import cast

from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.resume.services.resume_section_services import (
    create_resume_sections,
    delete_resume_sections,
    update_resume_sections,
)


@api_view(["POST", "PATCH", "DELETE"])
def resume_section_view(request: Request, resume_id: str):
    user = request.user
    data = cast(dict, request.data)

    if request.method == "POST":
        return create_resume_sections(user, data, resume_id)
    if request.method == "PATCH":
        return update_resume_sections(user, data, resume_id)
    if request.method == "DELETE":
        return delete_resume_sections(user, data, resume_id)
