from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):

    email = models.EmailField(("email address"), blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
    def __str__(self) -> str :
        return self.username

class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)

    def __str__(self) -> str :
        return self.user.username