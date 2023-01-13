from abc import ABC

from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from cookiecutter.users.models import AppUser


class AppUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser

        return token


class RegisterRequestSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class RegisterResponseSerializer(Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserGroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(ModelSerializer):
    groups = UserGroupSerializer(many=True, read_only=True)

    class Meta:
        model = AppUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "date_joined",
            "is_active",
        )