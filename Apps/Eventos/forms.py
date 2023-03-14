from django import forms
from Apps.Eventos.models import Event, EventParticipant, Career
from django_countries.fields import CountryField
from django.utils import timezone
from django.forms import ValidationError

gender_options = [
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
]

modality_options = [
    ('Presencial', 'Presencial'),
    ('Online', 'Online'),
    ('Online y Presencial', 'Online y Presencial'),
]


class CareerForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Educación',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))

    class Meta:
        model = Career
        exclude = ['date_created']


class EventForm(forms.ModelForm):
    logo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'accept': 'image/jpeg, image/jpg',
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
    }))
    title = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Seminario de...',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    place = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Instituto Deming...',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    addressed_to = forms.CharField(max_length=300, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Personas interesadas en aprender sobre...',
        'rows': '3',
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    price = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': '123.12',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    final_date = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    modality = forms.ChoiceField(choices=modality_options, required=True, widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    country_phone = CountryField(help_text='Este país será utilizado para saber el '
                                           'código de marcación correspondiente a número de teléfono').formfield()
    phone = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': '9999999999',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    alternative_phone = forms.CharField(required=False, widget=forms.NumberInput(attrs={
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
    curriculum_user = forms.FileField(required=True, widget=forms.FileInput(attrs={
        'accept': 'application/pdf, application/vnd.ms-excel',
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
    }))
    event_planning = forms.FileField(required=True, widget=forms.FileInput(attrs={
        'accept': 'application/pdf, application/vnd.ms-excel',
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
    }))
    link_video = forms.URLField(max_length=150, required=False, widget=forms.URLInput(attrs={
        'placeholder': 'https://example.com',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    career = forms.ModelChoiceField(required=False, queryset=Career.objects.all(), widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        current_date = timezone.now().date()
        if start_date < current_date:
            raise ValidationError("La fecha de inicio no puede ser menor que la fecha actual.")
        return start_date

    def clean_final_date(self):
        final_date = self.cleaned_data.get('final_date')
        current_date = timezone.now().date()

        if final_date < current_date:
            raise ValidationError("La fecha final no puede ser menor que la fecha actual.")
        return final_date

    class Meta:
        model = Event
        exclude = ['user', 'date_created', 'active']
        help_texts = {
            'country_phone': 'Este país será utilizado para saber el código de marcación correspondiente a número de teléfono',
        }


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
