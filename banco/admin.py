from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import CustomUsuarioChangeForm, CustomUsuarioCreateForm

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form =  CustomUsuarioChangeForm
    model = Usuario
    list_display = ('id', 'username', 'cpf', 'saldo', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Seção padrão de login
        ('Informações Pessoais', {'fields': ('cpf', 'endereco', 'genero')}),  # Substituindo os campos
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Permissões
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),  # Datas padrão do Django
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Informações Pessoais', {'fields': ('cpf', 'endereco', 'genero')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

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

