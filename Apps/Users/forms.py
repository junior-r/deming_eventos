from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from Apps.Users.models import User


class UserForm(UserCreationForm):
    profile_image = forms.ImageField(label='Imagen de perfil', required=False, widget=forms.FileInput(
        attrs={
            'class': 'inputfile inputfile-5',
            'id': 'file-5',
            'data-multiple-caption': '{count} archivos seleccionados',
        }
    ))
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Nombre de usuario')
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Dirección de correo eletrónico')
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Nombres')
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Apellidos')

    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Contraseña')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Contraseña (confirmación)')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario registrado con este email. Intente con otro.")
        return email

    class Meta:
        model = User
        fields = ['profile_image', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    user_id = forms.CharField(required=True, widget=forms.NumberInput(attrs={'hidden': True}))
    profile_image = forms.ImageField(label='Imagen de perfil', required=False, widget=forms.FileInput(
        attrs={
            'class': 'inputfile inputfile-5',
            'id': 'file-5',
            'data-multiple-caption': '{count} archivos seleccionados',
        }
    ))
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Nombre de usuario')
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Dirección de correo eletrónico')
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Nombres')
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Apellidos')

    def _clean_fields(self):
        email = self.cleaned_data.get('email')
        user_id = self.cleaned_data.get('user_id')
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("Ya existe un usuario registrado con este email. Intente con otro.")
        return email

    class Meta:
        model = User
        fields = ['user_id', 'profile_image', 'username', 'first_name', 'last_name', 'email']
