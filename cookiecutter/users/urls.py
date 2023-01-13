from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cookiecutter.users.views import UsersViewSet, GroupsViewSet

router = DefaultRouter()
router.register("groups", GroupsViewSet)
router.register("", UsersViewSet)

urlpatterns = [
    path("", include(router.urls)),
]