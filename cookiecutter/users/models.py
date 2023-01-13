import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from cookiecutter.users.user_manager import AppUserManager


class AppUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def __str__(self):
        return f'{self.email}'
