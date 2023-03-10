from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AppUser


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AppUser
        fields = ("email", "groups")


class AppUserChangeForm(UserChangeForm):
    class Meta:
        model = AppUser
        fields = ("email", "groups")