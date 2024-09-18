from abc import ABC

from django.contrib.auth.models import Group, Permission
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
        token["groups"] = UserGroupSerializer(user.groups.all(), many=True).data

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


class UpdateMyProfileRequestSerializer(Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

class MyProfileRequestSerializer(Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class UserGroupSerializer(ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = "__all__"


class BasicUserSerializer(ModelSerializer):
    class Meta:
        model = AppUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )

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