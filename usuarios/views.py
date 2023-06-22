from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import auth
from django.contrib.messages import constants
from .models import Users, Ativacao
from .utils import email_html
import os
from django.conf import settings
import re
from hashlib import sha256

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    
    if request.user.is_authenticated:
        return redirect('/pacientes')

    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

    if not senha == confirmar_senha:
        messages.add_message(request, constants.WARNING, "As senhas não são iguais!")
        return redirect(reverse('cadastro'))

    charCheck = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d).*$')
    passwordCheck = re.fullmatch(charCheck, senha)

    if passwordCheck == None:
        messages.add_message(request, constants.WARNING, "A senha precisa conter letras e números!")
        return redirect(reverse('cadastro'))

    user = Users.objects.filter(email=email)
    
    if user.exists():
        messages.add_message(request, constants.ERROR, "Este email já está cadastrado!")
        return redirect(reverse('cadastro'))
    try:
        user = Users.objects.create_user(
            username=nome,
            email=email,
            password=senha,
            is_active=False
        )
        user.save()

        token = sha256(f"{nome}{email}".encode()).hexdigest()
        ativacao = Ativacao(token=token, user=user)
        ativacao.save()

        path_template = os.path.join(settings.BASE_DIR, 'usuarios/templates/emails/cadastro_confirmado.html')
        email_html(path_template, 'Cadastro confirmado', [email,], username=nome, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")
        messages.add_message(request, constants.SUCCESS, "Verifique seu email para finalizar o cadastro!")
        return redirect(reverse('login'))
    except:
        messages.add_message(request, constants.ERROR, "Erro interno do sistema")
        return redirect(reverse('cadastro'))

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    if request.user.is_authenticated:
        return redirect('/pacientes')
    
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        
        user = auth.authenticate(username=email, password=senha)
        
        if not user:
            messages.add_message(request, constants.ERROR, "Email ou senha incorretos!")
            return redirect(reverse('login'))

        auth.login(request, user)
        return redirect('/pacientes/')

def sair(request):
    auth.logout(request)
    messages.add_message(request, constants.WARNING, "Faça login antes de acessar a plataforma!")
    return redirect(reverse('login'))

def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, constants.ERROR, "Este token já foi usado")
        return redirect('/auth/login')
    user = Users.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, "Conta ativada com sucesso!")
    return redirect('/auth/login')

