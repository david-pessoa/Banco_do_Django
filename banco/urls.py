from banco import views as v
from django.urls import path
from .views import Login, Saldo

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('saldo/<int:usuario_id>', Saldo.as_view(), name='saldo')

]