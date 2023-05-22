from django import forms
from captcha.fields import ReCaptchaField
from django_countries.fields import CountryField
from Apps.Home.models import EmailContact, EmailContactEvent, WhatsAppContact


class EmailContactForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'placeholder': ' ',
        }
    ), label='Tu correo electrónico')
    subject = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={
            'placeholder': ' ',
        }
    ), label='Título de tu mensaje')
    message = forms.CharField(max_length=800, required=True, widget=forms.Textarea(
        attrs={
            'rows': 3,
            'placeholder': ' ',
        }
    ), label='Deja un mensaje...')
    captcha = ReCaptchaField()

    class Meta:
        model = EmailContact
        fields = ['email', 'subject', 'message', 'captcha']


class EmailContactEventForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
        }
    ), label='Tus Nombres')
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
        }
    ), label='Tu correo electrónico')
    title = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
        }
    ), label='Título de tu mensaje')
    message = forms.CharField(max_length=800, required=True, widget=forms.Textarea(
        attrs={
            'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'rows': 3,
            'placeholder': ' ',
        }
    ), label='Deja un mensaje...')
    captcha = ReCaptchaField()

    class Meta:
        model = EmailContactEvent
        fields = ['name', 'email', 'title', 'message', 'captcha']


class WhatsAppContactForm(forms.ModelForm):
    names = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
        }
    ), label='Tus Nombres')
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
        }
    ), label='Tu correo electrónico')
    country = CountryField(help_text=' Asegurate de seleccionar correctamente el país, ya que este será utilizado para el código de teléfono').formfield()
    phone = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={
            'class': 'block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer',
            'placeholder': ' ',
        }
    ), label='Tu número de teléfono')
    message = forms.CharField(max_length=800, required=True, widget=forms.Textarea(
        attrs={
            'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'rows': 3,
            'placeholder': ' ',
        }
    ), label='Deja un mensaje...')
    captcha = ReCaptchaField()

    class Meta:
        model = WhatsAppContact
        fields = ['names', 'email', 'country', 'phone', 'message', 'captcha']
