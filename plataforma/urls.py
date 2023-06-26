from django.urls import path, include
from . import views

urlpatterns = [
    path('pacientes/', views.pacientes, name="pacientes"),
    path('dados_paciente/', views.dados_paciente_listar, name="dados_paciente_listar"),
    path('dados_paciente/<int:id>', views.dados_paciente, name="dados_paciente"),
    path('grafico_peso/<int:id>/', views.grafico_peso, name="grafico_peso"),
    path('plano_alimentar_listar/', views.plano_alimentar_listar, name="plano_alimentar_listar"),
    path('plano_alimentar/<int:id>', views.plano_alimentar, name="plano_alimentar"),
    path('refeicao/<int:id_paciente>/', views.refeicao, name="refeicao"),
    path('opcao/<int:id_paciente>/', views.opcao, name="opcao"),

] 