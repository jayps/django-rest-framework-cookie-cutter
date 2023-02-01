from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cookiecutter.books.views import AuthorsViewSet, BooksViewSet
from cookiecutter.users.views import UsersViewSet, GroupsViewSet

router = DefaultRouter()
router.register("authors", AuthorsViewSet)
router.register("", BooksViewSet)

urlpatterns = [
    path("", include(router.urls)),
]