from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
    path('login/', views.login, name='login'),
    path('ativar_conta/<str:token>/', views.ativar_conta, name="ativar_conta"),
    path('sair/', views.sair, name="sair"),
]