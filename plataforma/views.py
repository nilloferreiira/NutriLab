from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Pacientes, DadosPaciente
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required(login_url='/auth/login')
def pacientes(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes': pacientes})

    elif request.method == "POST":
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/pacientes/')

        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
            return redirect('/pacientes/')

        pacientes = Pacientes.objects.filter(email=email)

        if pacientes.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('/pacientes/')

        try:
            paciente = Pacientes(
                nome=nome,
                sexo=sexo,
                idade=idade,
                email=email,
                telefone=telefone,
                nutri=request.user
            )
            paciente.save()

            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso!')
            return redirect('/pacientes/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
            return redirect('/pacientes/')

@login_required(login_url='/auth/login')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})

@login_required(login_url='/auth/login')
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, "Este paciente não é seu!")
        return redirect('dados_paciente')
    
    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
    
    elif request.method == "POST":
        altura = request.POST.get('altura')
        peso = request.POST.get('peso')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')
        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        ctotal = request.POST.get('ctotal')
        trigliceridios = request.POST.get('trigliceridios')

        if (len(altura.strip()) == 0) or (len(peso.strip()) == 0) or (len(gordura.strip()) == 0) or (len(musculo.strip()) == 0) or (len(hdl.strip()) == 0) or (len(ldl.strip()) == 0) or (len(ctotal.strip()) == 0) or (len(trigliceridios.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/dados_paciente/')

        try: 
            paciente = DadosPaciente(paciente=paciente,
                            data=datetime.now(),
                            peso=peso,
                            altura=altura,
                            gordura=gordura,
                            musculo=musculo,
                            hdl=hdl,
                            ldl=ldl,
                            ctotal=ctotal,
                            trigliceridios=trigliceridios)

            paciente.save()
            messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')
        except:
            messages.add_message(request, constants.ERROR, "Erro ao salvar os dados do paciente")
            return redirect('/dados_paciente/')
        return redirect(f'/dados_paciente/{id}')

@login_required(login_url='/auth/login')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data")

    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos, 'labels': labels}
    return JsonResponse(data)