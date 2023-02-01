# from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from cookiecutter.users.views import AppUserTokenObtainPairView, RegisterView

schema_view = get_schema_view(
   openapi.Info(
      title="Cookie Cutter API",
      default_version='v1',
      description="This is a base API.",
      contact=openapi.Contact(email="jp@jpmeyer.dev"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Auth
    path(
        "api/auth/login/",
        AppUserTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/register/", RegisterView.as_view()),
    # Apps
    path("api/users/", include("cookiecutter.users.urls")),
    path("api/books/", include("cookiecutter.books.urls")),
]