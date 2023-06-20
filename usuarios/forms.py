from django.contrib.auth import forms
from .models import Users
from django.contrib.auth.admin import UserAdmin

class UseChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Users

class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Users