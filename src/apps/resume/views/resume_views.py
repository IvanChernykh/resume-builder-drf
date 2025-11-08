from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.resume.serializers.resume_serializer import (
    CreateResumeSerializer,
    GetResumeSerializer,
    UpdateResumeSerializer,
)
from apps.resume.services.resume_services import (
    create_resume,
    delete_resume,
    get_all_user_resumes,
    get_resume,
    update_resume,
)
from utils.constants.drf_spectacular import AUTH_API_HEADER


@extend_schema(
    methods=["GET"],
    responses={200: GetResumeSerializer(many=True)},
)
@extend_schema(
    methods=["POST"],
    request=CreateResumeSerializer,
    responses={201: CreateResumeSerializer},
)
@extend_schema(parameters=[AUTH_API_HEADER])
@api_view(["Get", "POST"])
def resume_view(request: Request):
    if request.method == "GET":
        return get_all_user_resumes(request)

    if request.method == "POST":
        return create_resume(request)


@extend_schema(
    methods=["GET"],
    responses={200: GetResumeSerializer},
)
@extend_schema(
    methods=["PUT"],
    request=UpdateResumeSerializer,
    responses={200: UpdateResumeSerializer},
)
@extend_schema(
    methods=["DELETE"],
    responses={204: None},
)
@extend_schema(parameters=[AUTH_API_HEADER])
@api_view(["GET", "PUT", "DELETE"])
def resume_detail_view(request: Request, resume_id: str):
    if request.method == "GET":
        return get_resume(request, resume_id)

    if request.method == "PUT":
        return update_resume(request, resume_id)

    if request.method == "DELETE":
        return delete_resume(request, resume_id)
