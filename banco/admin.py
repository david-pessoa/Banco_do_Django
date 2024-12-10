from atexit import register
from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):
    list_display = (
        'id', 'email', 'username', 'is_staff'
    )

# Registre o modelo personalizado com o admin
admin.site.register(Usuario, UsuarioAdmin)
