from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import UserModel
from users.serializers import UserSerializer


@api_view(["GET"])
def me(request: Request):
    user = UserModel.objects.first()
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
