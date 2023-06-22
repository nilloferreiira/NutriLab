from django.db import models
from usuarios.models import Users

class Pacientes(models.Model):
    choices_sexo = (('F', 'Feminino'),
                    ('M', 'Masculino'))
    nome = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=choices_sexo)
    idade = models.IntegerField()
    email = models.EmailField()
    telefone = models.CharField(max_length=19)
    nutri = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class DadosPaciente(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data = models.DateTimeField()
    peso = models.FloatField()
    altura = models.IntegerField()
    gordura = models.FloatField()
    musculo = models.FloatField()
    hdl = models.FloatField()
    ldl = models.FloatField()
    ctotal = models.FloatField()
    trigliceridios = models.FloatField()

    def __str__(self):
        return f"Paciente({self.paciente.nome}, {self.peso})"