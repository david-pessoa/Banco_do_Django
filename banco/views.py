from multiprocessing import context
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from .models import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from decimal import Decimal
from .templatetags.money_field import format_money_back_end
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

class LoginView(View):
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


class SaldoView(LoginRequiredMixin, View):
    def get(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)
        if usuario.senha_pix == "":
            faz_pix = False
        else:
            faz_pix = True

        context = {
            "usuario": usuario,
            "faz_pix": faz_pix
        }

        return render(request, 'saldo.html', context)
    
    def post(self, request, usuario_id):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class SaqueView(LoginRequiredMixin, View):
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
        saque = Decimal(format_money_back_end(request.POST.get("saque")))

        context = {
            "usuario": usuario
        }
        usuario.saldo -= saque
        transacao = Transacoes(usuario=usuario, tipo='SAQUE', valor=saque)

        if usuario.saldo < 0:
            messages.error(request, "Não é possível retirar mais que o saldo disponível!")
            return render(request, 'saque.html', context)
        
        if saque <= 0:
            messages.error(request, "O valor do saque não deve ser menor ou igual a zero!")
            return render(request, 'saque.html', context)
        
        result = transacao.verifica(False)
        if result != True:
            messages.error(request, result)
            return render(request, 'saque.html', context)
        
        usuario.save()
        transacao.save()
        
        return HttpResponseRedirect(reverse('saldo', args=[usuario.pk]))

class DepositoView(LoginRequiredMixin, View):
    def get(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)
        context = {
            "usuario": usuario
        }
        return render(request, 'deposito.html', context)
    
    def post(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)
        deposito = Decimal(format_money_back_end(request.POST.get("deposito")))

        context = {
            "usuario": usuario
        }
        usuario.saldo += deposito
        transacao = Transacoes(usuario=usuario, tipo='DEPOSITO', valor=deposito)

        result = transacao.verifica(False)
        if result != True:
            messages.error(request, result)
            return render(request, 'deposito.html', context)

        if deposito <= 0:
            messages.error(request, "O valor do deposito não deve ser menor ou igual a zero!")
            return render(request, 'deposito.html', context)
        
        usuario.save()
        transacao.save()
        return HttpResponseRedirect(reverse('saldo', args=[usuario.pk]))

class CadastroView(View):
    def get(self, request):

        generos = Genero.objects.all()

        context = {
            "generos": generos
        }

        return render(request, 'cadastro.html', context)
    
    def post(self, request):
        try:
            nome = request.POST.get("nome")
            cpf = request.POST.get("cpf")
            email = request.POST.get("email")
            endereco = request.POST.get("endereco")
            genero = request.POST.get("genero")
            senha = request.POST.get("senha")
            genero = Genero.objects.get(pk=genero)

            novo_usuario = Usuario(
                username=nome,
                cpf=cpf,
                email=email,
                endereco=endereco,
                genero=genero,
                password=senha,
                saldo=0
            )

            result = novo_usuario.verifica()
            if result != True:
                generos = Genero.objects.all()
                context = {
                    "generos": generos
                }
                messages.error(request, result)
                return render(request, 'cadastro.html', context)

            novo_usuario.save()
            login(request, novo_usuario)

            return HttpResponseRedirect(reverse('saldo', args=[novo_usuario.pk]))
        
        except:
            messages.error(request, "Não foi possível cadastrar a pessoa. Verifique os dados e tente novamente")
            return render(request, 'cadastro.html')

class HistoricoView(View):
    def get(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)
        transferencias = Transacoes.objects.filter(usuario=usuario).order_by('-data')
    
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Ordenação (pegando o índice e a direção enviados pelo DataTables)
            print(int(request.GET.get("start", 0)))
            ordering_column_index = int(
                request.GET.get(
                    "order[0][column]", 0
                )  # Default é o 0. (Index da col data)
            )
            ordering_column = request.GET.get(
                f"columns[{ordering_column_index}][data]",
                "data",  # Default é a coluna data
            )
            ordering_direction = request.GET.get(
                "order[0][dir]", "asc"
            )  # Default é asc

            if ordering_direction not in ["asc", "desc"]:
                ordering_direction = "asc"
            
            # --- FORMATA E APLICA A ORDENAÇÃO DO QUERYSET CONFORME ESTRUTURA DE CADA COLUNA ---
            if ordering_column in [
                "tipo",
                "valor",
                "data",
            ]:  # Não podem usar a função Lower
                transferencias = transferencias.order_by(ordering_column)

            if ordering_direction == "desc":
                transferencias = transferencias.reverse()

             # Parâmetro de busca
            search_param = request.GET.get("search_param", "")
            data_param = False
            try:
                # Converte 'DD/MM/YYYY HH:MM' para 'YYYY-MM-DD HH:MM'
                local_dt = datetime.strptime(search_param, '%d/%m/%Y %H:%M')

                # Ajusta para UTC - 3
                utc_dt = local_dt + timedelta(hours=3)

                # Torna a data consciente de fuso horário
                utc_dt = make_aware(utc_dt)

                # Busca por datas contendo a string ISO formatada
                search_param = utc_dt.strftime('%Y-%m-%d %H:%M')
                data_param = True
            except ValueError:
                # Handle cases where parsing might fail
                data_param = False

            # 2025-01-06 16:21:44+00:00
            if search_param and data_param:
                transferencias = transferencias.filter(
                    Q(valor__icontains=search_param)
                    | Q(data__icontains=search_param)
                    | Q(tipo__icontains=search_param)
                )
            elif search_param:
                transferencias = transferencias.filter(
                    Q(valor__icontains=search_param)
                    | Q(tipo__icontains=search_param)
                )

            # Paginação
            page_number = int(request.GET.get("start", 0)) // int(request.GET.get("length", 10)) + 1
            paginator = Paginator(transferencias, int(request.GET.get("length", 10)))
            pagina = paginator.get_page(page_number).object_list

            # Formatar os dados para o DataTables
            data = [
                {
                    "tipo": transferencia.tipo,
                    "valor": transferencia.valor,
                    "data": timezone.localtime(transferencia.data).strftime("%d/%m/%Y %H:%M"),
                }
                for transferencia in pagina
            ]

            response = {
                "draw": int(request.GET.get("draw", 0)),
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": data,
            }
            return JsonResponse(response)
        
        else:
            context = {
                "transferencias": transferencias,
                "usuario": usuario,
            }
            return render(request, 'historico.html', context)

class CriaPIXView(View):
    def get(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)
        chave_celular = ChavePIX.objects.filter(usuario=usuario, tipo='CELULAR')
        chave_email = ChavePIX.objects.filter(usuario=usuario, tipo='EMAIL')
        chave_cpf = ChavePIX.objects.filter(usuario=usuario, tipo='CPF')
        LISTA_TIPOS = ChavePIX.TIPO_CHAVE_CHOICES
        
        lista_exibe = []
        for tipo in LISTA_TIPOS:
            lista_exibe.append(tipo[1])
        
        if chave_celular.count() != 0:
            lista_exibe.remove('Número de celular')
            chave_celular = chave_celular[0]
        else:
            chave_celular = None

        if chave_email.count() != 0:
            lista_exibe.remove('E-mail')
            chave_email = chave_email[0]
        else:
            chave_email = None
        
        if chave_cpf.count() != 0:
            lista_exibe.remove('CPF')
            chave_cpf = chave_cpf[0]
        else:
            chave_cpf = None

        if not chave_celular is None and not chave_email is None and not chave_cpf is None:
            cria = False
        else:
            cria = True
        
        if len(lista_exibe) == 3:
            cria_senha_pix = True
        else:
            cria_senha_pix = False

        context = {
            "usuario": usuario,
            "habilita": cria,
            "lista_tipos": lista_exibe,
            "cria_senha_pix": cria_senha_pix,
            "chave_celular": chave_celular,
            "chave_email": chave_email,
            "chave_cpf": chave_cpf,
        }

        return render(request, 'cria_chave.html', context)
    
    def post(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        result = ""
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            tipo_chave = request.POST.get("tipo_chave")
            chave_pix = request.POST.get("chave_pix")
            cria_senha_pix = request.POST.get("senha_pix")

            chave_celular = ChavePIX.objects.filter(usuario=usuario, tipo='CELULAR')
            chave_email = ChavePIX.objects.filter(usuario=usuario, tipo='EMAIL')
            chave_cpf = ChavePIX.objects.filter(usuario=usuario, tipo='CPF')

            if not chave_celular.exists() and not chave_email.exists() and not chave_cpf.exists():
                usuario.senha_pix = cria_senha_pix
                usuario.save()

            if tipo_chave == 'E-mail':
                tipo_chave = 'EMAIL'
            if tipo_chave == 'Número de celular':
                tipo_chave = 'CELULAR'

            nova_chave = ChavePIX(
                usuario=usuario,
                tipo=tipo_chave,
                valor=chave_pix,
            )
            result = nova_chave.verifica()
            if result != True:
                raise ValidationError(result)
            nova_chave.save()
            return HttpResponseRedirect(reverse('saldo', args=[usuario.pk]))
        except:
            if result == "":
                messages.error(request, "Não foi possível cadastrar a chave PIX")
            else:
                messages.error(request, result)
            chave_celular = ChavePIX.objects.filter(usuario=usuario, tipo='CELULAR')
            chave_email = ChavePIX.objects.filter(usuario=usuario, tipo='EMAIL')
            chave_cpf = ChavePIX.objects.filter(usuario=usuario, tipo='CPF')
            LISTA_TIPOS = ChavePIX.TIPO_CHAVE_CHOICES
        
            lista = []
            for tipo in LISTA_TIPOS:
                lista.append(tipo[1])
            
            if chave_celular.count() != 0:
                lista.remove('Número de celular')
                chave_celular = chave_celular[0]
            else:
                chave_celular = None

            if chave_email.count() != 0:
                lista.remove('E-mail')
                chave_email = chave_email[0]
            else:
                chave_email = None

            if chave_cpf.count() != 0:
                lista.remove('CPF')
                chave_cpf = chave_cpf[0]
            else:
                chave_cpf = None
    
            if not chave_celular is None and not chave_email is None and not chave_cpf is None:
                cria = False
            else:
                cria = True

            if len(lista) == 3:
                cria_senha_pix = True
            else:
                cria_senha_pix = False
    
            context = {
                "usuario": usuario,
                "habilita": cria,
                "lista_tipos": lista,
                "cria_senha_pix": cria_senha_pix,
                "chave_celular": chave_celular,
                "chave_email": chave_email,
                "chave_cpf": chave_cpf,
            }

            return render(request, 'cria_chave.html', context)

class RealizaPixView(View):
    def get(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        usuario = Usuario.objects.get(pk=usuario_id)

        context = {
            "usuario": usuario,
        }

        return render(request, 'realiza.html', context)
    
    def post(self, request, usuario_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        usuario = Usuario.objects.get(pk=usuario_id)

        context = {
                "usuario": usuario,
            }
        result = ""
        try:
            valor_pix = Decimal(format_money_back_end(request.POST.get("valor_pix")))
            senha_pix = request.POST.get("senha_pix")
            chave_pix_recebedor = request.POST.get("chave_recebedor")

            if valor_pix <= 0:
                messages.error(request, "O valor do pix não deve ser maior que zero!")
                return render(request, 'realiza.html', context)
            
            if usuario.saldo - valor_pix < 0:
                messages.error(request, "O valor do pix não pode exceder o saldo!")
                return render(request, 'realiza.html', context)
            
            if usuario.senha_pix != senha_pix:
                messages.error(request, "Senha incorreta!")
                return render(request, 'realiza.html', context)
            
            usuario.saldo -= valor_pix
            transacao = Transacoes(usuario=usuario, tipo='PAGAMENTO PIX', valor=valor_pix, chave_pix=chave_pix_recebedor)
            result = transacao.verifica(True)
            if result != True:
                raise ValidationError(result)

            transacao.save()
            usuario.save()
            return HttpResponseRedirect(reverse('saldo', args=[usuario.pk]))
        
        except:
            if result == "":
                messages.error(request, "Não foi possível realizar o PIX. Verifique os dados e tente novamente")
            else:
                messages.error(request, result)

            return render(request, 'realiza.html', context)