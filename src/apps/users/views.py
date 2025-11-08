from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import UserModel
from apps.users.serializers import UserSerializer
from utils.constants.drf_spectacular import AUTH_API_HEADER


@extend_schema(
    methods=["GET"],
    responses={200: UserSerializer},
    parameters=[AUTH_API_HEADER],
)
@api_view(["GET"])
def me(request: Request):
    user = UserModel.objects.first()
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
