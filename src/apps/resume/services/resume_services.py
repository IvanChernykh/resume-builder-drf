from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.resume.serializers.resume_serializer import CreateResumeSerializer


def create_resume(request: Request):
    serializer = CreateResumeSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
