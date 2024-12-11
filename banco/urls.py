from banco import views as v
from django.urls import path
from .views import login

urlpatterns = [
    path('', login, name='login')
]