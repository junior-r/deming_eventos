from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField

from Apps.Eventos.models import Career
from Apps.Users.models import User


class UserForm(UserCreationForm):
    captcha = ReCaptchaField()
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
    ), label='Nombre de usuario*', required=True)
    profession = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Profesión*', required=True)
    curriculum = forms.FileField(required=True, widget=forms.FileInput(attrs={
        'accept': 'application/pdf, application/vnd.ms-excel',
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
    }), label='Hoja de vida (PDF)*')
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Dirección de correo eletrónico*', required=True)
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Nombres*', required=True)
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Apellidos*', required=True)

    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Contraseña*', required=True)
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Contraseña (confirmación)*', required=True)
    interests = forms.ModelMultipleChoiceField(queryset=Career.objects.all(), required=False, widget=forms.SelectMultiple(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }), label='¿Cuáles son tus intereses?')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario registrado con este email. Intente con otro.")
        return email

    class Meta:
        model = User
        fields = ['profile_image', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'profession', 'curriculum', 'interests']


class UpdateUserForm(forms.ModelForm):
    captcha = ReCaptchaField()
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
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 '
                     'focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 '
                     'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Nombre de usuario')
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 '
                     'focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 '
                     'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Dirección de correo eletrónico')
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 '
                     'focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 '
                     'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Nombres')
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 '
                     'focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 '
                     'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Apellidos')
    profession = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 '
                     'focus:border-blue-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 '
                     'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
        }
    ), label='Profesión')
    curriculum = forms.FileField(required=True, widget=forms.FileInput(attrs={
        'accept': 'application/pdf, application/vnd.ms-excel',
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 '
                 'dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400',
    }), label='Hoja de vida (PDF)')
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 '
                     'dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 '
                     'dark:border-gray-600',
        }
    ), label='¿Es staff?')
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 '
                     'dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 '
                     'dark:border-gray-600',
        }
    ), label='¿Está activo?')
    is_teacher = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 '
                     'dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 '
                     'dark:border-gray-600',
        }
    ), label='¿Es Ponente?')
    is_referral = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 '
                     'dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 '
                     'dark:border-gray-600',
        }
    ), label='¿Es Reclutador?')
    interests = forms.ModelMultipleChoiceField(queryset=Career.objects.all(), required=False, widget=forms.SelectMultiple(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 '
                 'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 '
                 'dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }), label='¿Cuáles son tus intereses?')

    def clean(self):
        cleaned_data = super().clean()

        # Clean email
        email = cleaned_data.get('email')
        user_id = cleaned_data.get('user_id')
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("Ya existe un usuario registrado con este email. Intente con otro.")
        return cleaned_data

    class Meta:
        model = User
        fields = ['user_id', 'profile_image', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',
                  'is_teacher', 'profession', 'curriculum', 'is_referral', 'interests']
