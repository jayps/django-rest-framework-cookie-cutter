import uuid

from django.db import models

from cookiecutter.users.models import AppUser


# This is a demo model to show some interaction with the user.
# You can delete the entire books directory and remove it from `INSTALLED_APPS` in the settings file.
# Unless you're building an app for a library, then you might want to extend this a bit.


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255, null=False, blank=False)
    is_checked_out = models.BooleanField(default=False, blank=True, null=False)
    on_loan_to = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='loaned_books')
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
