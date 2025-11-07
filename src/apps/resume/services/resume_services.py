from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.resume.models import ResumeModel
from apps.resume.serializers.resume_serializer import (
    CreateResumeSerializer,
    GetResumeSerializer,
    UpdateResumeSerializer,
)


def create_resume(request: Request):
    serializer = CreateResumeSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_all_user_resumes(request: Request):
    resumes = ResumeModel.objects.filter(owner=request.user)

    serializer = GetResumeSerializer(resumes, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


def get_resume(request: Request, resume_id: str):
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=request.user)
    serializer = GetResumeSerializer(resume)

    return Response(serializer.data, status=status.HTTP_200_OK)


def update_resume(request: Request, resume_id: str):
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=request.user)
    serializer = UpdateResumeSerializer(instance=resume, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_resume(request: Request, resume_id: str):
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=request.user)
    resume.delete()

    return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)
