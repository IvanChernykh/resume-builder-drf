from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.users.models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["name", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])

        user = UserModel.objects.create(**validated_data)
        return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password too short")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(max_length=128)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password too short")
        return value


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, max_length=128)
