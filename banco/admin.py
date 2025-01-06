from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'cpf', 'saldo', 'is_staff')  # Adicione 'cpf' aqui para ser exibido na lista
    

# Registre o modelo personalizado com o admin

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'genero'
    )

@admin.register(ChavePIX)
class ChavePIXAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'usuario', 'tipo', 'valor'
    )

@admin.register(Transacoes)
class TransacoesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "usuario", "tipo", "valor", "data"
    )

