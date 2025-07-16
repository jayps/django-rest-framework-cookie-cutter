from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError, transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from cookiecutter.users.models import AppUser
from cookiecutter.users.serializers import (
    AppUserTokenObtainPairSerializer,
    RegisterRequestSerializer,
    UserSerializer,
    RegisterResponseSerializer,
    UserGroupSerializer, UpdateMyProfileRequestSerializer, PermissionSerializer, CreateUserGroupSerializer,
    UserGroupDetailSerializer,
)


class AppUserTokenObtainPairView(TokenObtainPairView):
    serializer_class = AppUserTokenObtainPairSerializer


def set_auth_cookies(response, access_token: str, refresh_token: str):
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=access_token,
        httponly=True,
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
        value=refresh_token,
        httponly=True,
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )

def clear_auth_cookies(response):
    response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
    response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({'success': True})
            set_auth_cookies(response, access_token, refresh_token)
            return response
        return Response(
            {'error': 'The username or password you have entered is incorrect.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            if token:
                token_obj = RefreshToken(token)
                token_obj.blacklist()
        except TokenError:
            pass  # Already invalid or blacklisted

        response = Response({'success': True})
        clear_auth_cookies(response)
        return response


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        if not refresh_token:
            return Response({'error': 'No refresh token'}, status=401)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)  # in case rotation is enabled

            response = Response({'success': True})
            set_auth_cookies(response, access_token, new_refresh_token)
            return response
        except TokenError:
            return Response({'error': 'Invalid refresh token'}, status=401)


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


class AllUsersViewSet(ReadOnlyModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = None
    search_fields = ("first_name", "last_name", "email")
    ordering_fields = ("first_name", "last_name", "email", "date_joined")
    filterset_fields = ("is_active", "is_superuser", "is_staff")


class MyProfileView(APIView):
    @swagger_auto_schema(operation_description="Get the current user profile.",
                         responses={200: UserSerializer(many=False)})
    def get(self, request):
        user = AppUser.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user, many=False)
        return Response(data=serializer.data)

    @swagger_auto_schema(operation_description="Update the current user profile.",
                         request_body=UpdateMyProfileRequestSerializer, responses={200: "Profile updated."})
    def patch(self, request):
        serializer = UpdateMyProfileRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("email") and \
                serializer.validated_data.get("email") != self.request.user.email and \
                AppUser.objects.filter(email=serializer.validated_data.get("email")).count() > 0:
            return Response(data="The requested email address is already in use.",
                            status=status.HTTP_412_PRECONDITION_FAILED)

        AppUser.objects.filter(id=self.request.user.id).update(**serializer.validated_data)

        return Response(data="Profile updated.", status=status.HTTP_200_OK)


class GroupsViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = (IsAdminUser,)
    search_fields = ("name",)
    ordering_fields = ("name",)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserGroupSerializer
        elif self.action == 'retrieve':
            return UserGroupDetailSerializer
        else:
            return CreateUserGroupSerializer


class PermissionsViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = None
