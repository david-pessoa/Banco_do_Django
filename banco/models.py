from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Genero(models.Model):
    genero = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.genero

class Usuario(AbstractUser):
    endereco = models.CharField("Endereço", max_length= 100, default="")
    cpf = models.CharField("CPF", max_length=14, default="")
    saldo = models.DecimalField("Saldo", decimal_places=2, max_digits=10, validators=[MinValueValidator(0)], default=0)

    def checa_senha(self, senha):
        return self.password == senha

class ChavePIX(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario")
    TIPO_CHAVE_CHOICES = [
        ('EMAIL', 'E-mail'),
        ('CPF', 'CPF'),
        ('CELULAR', 'Número de celular'),
    ]
    tipo = models.CharField("Tipo de chave PIX", max_length=20, choices=TIPO_CHAVE_CHOICES, default='CPF')
    valor = models.CharField("Valor da chave PIX", max_length=30)

    def __str__(self):
        return self.tipo + ": " + self.valor



    