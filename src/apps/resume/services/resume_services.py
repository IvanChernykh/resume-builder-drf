from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apps.resume.models import ResumeModel
from apps.resume.serializers.resume_serializer import (
    CreateResumeSerializer,
    GetResumeSerializer,
    GetResumeDetailSerializer,
    UpdateResumeSerializer,
)
from apps.users.models import UserModel


def create_resume(user: UserModel, data: dict):
    serializer = CreateResumeSerializer(data=data, context={"user": user})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_all_user_resumes(user: UserModel):
    resumes = ResumeModel.objects.filter(owner=user)

    serializer = GetResumeSerializer(resumes, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


def get_resume(user: UserModel, resume_id: str):
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=user)
    serializer = GetResumeDetailSerializer(resume)

    return Response(serializer.data, status=status.HTTP_200_OK)


def update_resume(data: dict, user: UserModel, resume_id: str):
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=user)
    serializer = UpdateResumeSerializer(instance=resume, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_resume(user: UserModel, resume_id: str):
    resume = get_object_or_404(ResumeModel, pk=resume_id, owner=user)
    resume.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
