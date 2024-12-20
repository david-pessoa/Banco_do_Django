from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .templatetags.valida import valida_CPF, valida_numero, valida_email

class Genero(models.Model):
    genero = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.genero

class Usuario(AbstractUser):
    endereco = models.CharField("Endereço", max_length= 100, default="")
    cpf = models.CharField("CPF", max_length=14, default="")
    saldo = models.DecimalField("Saldo", decimal_places=2, max_digits=10, validators=[MinValueValidator(0)], default=0)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name="usuarios", default=1)
    senha_pix = models.CharField("Senha do pix", max_length=19, default="")

    def checa_senha(self, senha):
        return self.password == senha
    
    def verifica(self):
        #Verifica se o Gênero é válido
        if not isinstance(self.genero, Genero):
            return "Gênero ineválido"
        
        return valida_CPF(self.cpf)


class Transacoes(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="transacoes")
    TIPO_TRANSACOES = [
        ('SAQUE', 'Saque'),
        ('DEPOSITO', 'Depósito'),
        ('PAGAMENTO PIX', 'Pagamento PIX')
    ]
    tipo = models.CharField("Tipo de transação", max_length=20, choices=TIPO_TRANSACOES)
    valor = models.DecimalField("Valor", decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])
    data = models.DateTimeField("Data e horário da transação", auto_now_add=True)
    chave_pix = models.CharField("Chave pix do recebedor", max_length=30, default="")

    def verifica(self, eh_pix):
        #Verifica se o usuário está cadastrado no sistema
        if not isinstance(self.usuario, Usuario):
            return "Usuário não cadastrado no sistema"

        #Verifica se o tipo de transação é válido
        if self.tipo not in ['SAQUE', 'DEPOSITO', 'PAGAMENTO PIX']:
            return "Tipo de transação inválido"
        
        #Verifica se o valor da transação é válido
        if self.valor <= 0:
            return "O valor da transação deve ser maior que zero!"
        
        if valida_CPF(self.chave_pix) != True and valida_email(self.chave_pix) != True and valida_numero(self.chave_pix) != True and eh_pix:
            return "Chave pix inválida"
        
        return True

    def save(self, *args, **kwargs):
        # Impede alterações em objetos existentes
        if self.pk is not None:
            raise ValidationError("Transações existentes não podem ser alteradas.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"


class ChavePIX(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario")
    TIPO_CHAVE_CHOICES = [
        ('EMAIL', 'E-mail'),
        ('CPF', 'CPF'),
        ('CELULAR', 'Número de celular'),
    ]
    tipo = models.CharField("Tipo de chave PIX", max_length=20, choices=TIPO_CHAVE_CHOICES, default='CPF')
    valor = models.CharField("Valor da chave PIX", max_length=30)

    def verifica(self):
        #Verifica se o tipo de chave PIX é válido
        if self.tipo not in ['EMAIL', 'CPF', 'CELULAR']:
            return "Tipo de chave PIX inválido"
        
        #Verifica se o usuário está cadastrado no sistema
        if not isinstance(self.usuario, Usuario):
            return "Usuário não cadastrado no sistema"
        
        if valida_CPF(self.valor) != True and valida_email(self.valor) != True and valida_numero(self.valor) != True:
            return "Chave pix inválida"
        
        return True
        

    def __str__(self):
        return self.tipo + ": " + self.valor



    