from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.users.models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["name", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # TODO: add salt
        validated_data["password"] = make_password(validated_data["password"])

        user = UserModel.objects.create(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
