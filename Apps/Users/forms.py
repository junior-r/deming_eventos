from django import forms
from django.contrib.auth.forms import UserCreationForm

from Apps.Users.models import User


class UserFrom(UserCreationForm):
    profile_image = forms.ImageField(label='Imagen de perfil', required=False, widget=forms.FileInput(
        attrs={
            'class': '',
        }
    ))
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': ''
        }
    ), label='Nombre de usuario')
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': ''
        }
    ), label='Nombres')
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': ''
        }
    ), label='Apellidos')

    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': ''
        }
    ), label='Contraseña')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': ''
        }
    ), label='Contraseña (confirmación)')

    class Meta:
        model = User
        fields = ['profile_image', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']
