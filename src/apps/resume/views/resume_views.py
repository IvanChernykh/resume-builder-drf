from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.resume.serializers.resume_serializer import CreateResumeSerializer


@api_view(["POST"])
def create_resume(request: Request):
    serializer = CreateResumeSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
