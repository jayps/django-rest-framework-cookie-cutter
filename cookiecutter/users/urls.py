from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cookiecutter.users.views import UsersViewSet, GroupsViewSet, MyProfileView, PermissionsViewSet, AllUsersViewSet

router = DefaultRouter()
router.register("permissions", PermissionsViewSet)
router.register("groups", GroupsViewSet)
router.register("all", AllUsersViewSet)
router.register("", UsersViewSet)

urlpatterns = [
    path("my-profile/", MyProfileView.as_view()),
    path("", include(router.urls)),
]