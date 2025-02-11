from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import CustomUsuarioChangeForm, CustomUsuarioCreateForm

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    add_form = CustomUsuarioCreateForm
    form =  CustomUsuarioChangeForm
    model = Usuario
    list_display = ('id', 'username', 'cpf', 'saldo', 'is_staff')  # Adicione 'cpf' aqui para ser exibido na lista
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('cpf', 'endereco', 'genero')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

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

