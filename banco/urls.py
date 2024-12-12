from banco import views as v
from django.urls import path
from .views import *

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('cadastro', Cadastro.as_view(), name='cadastro'),
    path('saldo/<int:usuario_id>', Saldo.as_view(), name='saldo'),
    path('saque/<int:usuario_id>', Saque.as_view(), name='saque'),

]