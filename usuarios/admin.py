from django.contrib import admin
from .models import Users, Ativacao
from .forms import UseChangeForm, UserCreationForm
from django.contrib.auth import admin as admin_auth_django

@admin.register(Users)
class UsersAdmin(admin_auth_django.UserAdmin):
    form = UseChangeForm
    add_form = UserCreationForm
    model = Users

admin.site.register(Ativacao)