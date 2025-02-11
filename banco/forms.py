from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from .models import Usuario


class CustomUsuarioCreateForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'genero', 'password1', 'password2')
        labels = {'username': 'Nome de usuário'}

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data["password1"]
        user.set_password(password1)
        user.username = self.cleaned_data["username"]
        user.endereco = self.cleaned_data["endereco"]
        user.genero = self.cleaned_data["genero"]
        if commit:
            user.save()
        return user


class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = ('endereco', 'genero', 'username', 'cpf', 'password')