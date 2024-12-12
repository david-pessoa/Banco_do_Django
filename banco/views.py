from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import Usuario
from django.contrib import messages
from django.core.exceptions import ValidationError

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('saldo', args=[request.user.pk]))

        usuarios = Usuario.objects.all()

        context = {
            "usuarios": usuarios
        }
        return render(request, 'login.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            pass

        try:
            cpf = request.POST.get("cpf")
            senha = request.POST.get("senha")
            usuario = Usuario.objects.get(cpf=cpf)

            if usuario is not None and usuario.is_active and usuario.checa_senha(senha):
                login(request, usuario)
                return HttpResponseRedirect(reverse('saldo', args=[usuario.pk]))
            else:
                messages.error(request, "CPF ou senha incorretos!")
                
        except Exception as e:
            messages.error(request, "CPF ou senha incorretos!")
        
        return render(request, 'login.html')


class Saldo(View):
    def get(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)

        context = {
            "usuario": usuario
        }

        return render(request, 'saldo.html', context)

class Saque(LoginRequiredMixin, View):
    def get(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)
        context = {
            "usuario": usuario
        }
        return render(request, 'saque.html', context)
    
    def post(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)
        saque = request.POST.get("saque")

        context = {
            "usuario": usuario
        }
        usuario.saldo -= saque

        if usuario.saldo < 0:
            messages.error(request, "Não é possível retirar mais que o saldo disponível!")
            return render(request, 'saque.html', context)
        
        if saque <= 0:
            messages.error(request, "O valor do saque não deve ser menor ou igual a zero!")
            return render(request, 'saque.html', context)
        
        usuario.save()
        
        return render(request, 'saldo.html', context)

class Cadastro(View):
    def get(self, request):
        return render(request, 'cadastro.html')

