from typing import cast
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.resume.serializers.resume_section_serializer import (
    CreateSectionsSerializer,
    DeleteSectionsSerializer,
    UpdateSectionsSerializer,
)
from apps.resume.serializers.resume_serializer import GetResumeDetailSerializer
from apps.resume.services.resume_section_services import (
    copy_resume_sections,
    create_resume_sections,
    delete_resume_sections,
    update_resume_sections,
)
from utils.constants.drf_spectacular import AUTH_API_HEADER


@extend_schema(methods=["POST"], request=CreateSectionsSerializer)
@extend_schema(methods=["PATCH"], request=UpdateSectionsSerializer)
@extend_schema(methods=["DELETE"], request=DeleteSectionsSerializer)
@extend_schema(parameters=[AUTH_API_HEADER], responses={200: GetResumeDetailSerializer})
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


@api_view(["POST"])
def resume_section_copy_view(request: Request, resume_id: str):
    user = request.user
    data = cast(dict, request.data)

    return copy_resume_sections(user, data, resume_id)
