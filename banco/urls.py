from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('cadastro', CadastroView.as_view(), name='cadastro'),
    path('saldo/<int:usuario_id>', SaldoView.as_view(), name='saldo'),
    path('saque/<int:usuario_id>', SaqueView.as_view(), name='saque'),
    path('deposito/<int:usuario_id>', DepositoView.as_view(), name='deposito'),
    path('historico/<int:usuario_id>', HistoricoView.as_view(), name='historico'),
    path('criachavepix/<int:usuario_id>', CriaPIXView.as_view(), name='cria_chave'),
    path('realizapix/<int:usuario_id>', RealizaPixView.as_view(), name='realiza'),

]