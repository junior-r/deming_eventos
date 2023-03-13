from django import forms
from Apps.Eventos.models import EventParticipant
from django_countries.fields import CountryField

gender_options = [
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
]


class EventParticipantForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput(attrs={}))
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'John Jake',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Doe Smith',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    country_of_birth = CountryField().formfield()
    dni = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': '9999999999999',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    passport_number = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': '000000001',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    gender = forms.ChoiceField(choices=gender_options, required=True, widget=forms.Select(attrs={

    }))
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'class': '',
    }))
    current_country = CountryField().formfield()
    address = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Street address',
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    phone = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': '9999999999',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'johndoe@example.com',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    alternative_email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'johndoe123@example.com',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    profession = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Teacher',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    curriculum = forms.FileField(required=True, widget=forms.FileInput(attrs={

    }))
    object = forms.CharField(max_length=256, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'I want to be at the event, because...',
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))

    class Meta:
        model = EventParticipant
        exclude = ['date_created', 'active']


class DateInput(forms.DateInput):
    input_type = 'date'
