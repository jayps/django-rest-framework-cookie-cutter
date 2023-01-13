from django.contrib.auth.models import Group
from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from cookiecutter.users.models import AppUser
from cookiecutter.users.serializers import (
    AppUserTokenObtainPairSerializer,
    RegisterRequestSerializer,
    UserSerializer,
    RegisterResponseSerializer,
    UserGroupSerializer,
)


class AppUserTokenObtainPairView(TokenObtainPairView):
    serializer_class = AppUserTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = ()

    @swagger_auto_schema(
        request_body=RegisterRequestSerializer,
        responses={
            201: RegisterResponseSerializer(many=False),
            400: openapi.Response("Invalid request"),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Endpoint to register new users.
        """
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            created_user = AppUser.objects.create(
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                email=serializer.validated_data.get("email"),
            )
            created_user.set_password(serializer.validated_data.get("password"))
            created_user.save()
        except IntegrityError:
            return Response(
                data="The email address you've selected is already in use.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = UserSerializer(created_user)
        return Response(data=result.data, status=status.HTTP_201_CREATED)


class UsersViewSet(ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    search_fields = ("first_name", "last_name", "email")
    ordering_fields = ("first_name", "last_name", "email", "date_joined")
    filterset_fields = ("is_active", "is_superuser", "is_staff")


class GroupsViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = (IsAdminUser,)
    search_fields = ("name",)
    ordering_fields = ("name",)
