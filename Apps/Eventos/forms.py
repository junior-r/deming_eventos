from django import forms
from django.forms import ValidationError
from django.utils import timezone
from django_countries.fields import CountryField
from captcha.fields import ReCaptchaField

from Apps.Users.models import User
from Apps.Eventos.models import Event, Career, Participant

gender_options = [
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
]

modality_options = [
    ('Presencial', 'Presencial'),
    ('Online', 'Online'),
    ('Online y Presencial', 'Online y Presencial'),
]

platform_options = [
    ('', ''),
    ('Zoom', 'Zoom'),
    ('Google Meet', 'Google Meet'),
    ('Microsoft Teams', 'Microsoft Teams'),
    ('Discord', 'Discord'),
    ('Skype', 'Skype'),
]


class CareerForm(forms.ModelForm):
    captcha = ReCaptchaField()
    name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Educación',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))

    class Meta:
        model = Career
        exclude = ['date_created']


class EventForm(forms.ModelForm):
    captcha = ReCaptchaField(required=True)
    logo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'accept': 'image/jpeg, image/jpg, image/png',
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
    }))
    title = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Seminario de...',
        'class': 'required-field bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    place = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Ecuador',
        'class': 'required-field bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    addressed_to = forms.CharField(max_length=300, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Personas interesadas en aprender sobre...',
        'rows': 4,
        'class': 'required-field block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    price = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': '123.12',
        'step': 0.01,
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'min': timezone.now().date().isoformat(),
        'class': 'required-field bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    final_date = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'min': timezone.now().date().isoformat(),
        'class': 'required-field bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    modality = forms.ChoiceField(choices=modality_options, required=True, widget=forms.Select(attrs={
        'class': 'required-field bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    country_phone = CountryField(help_text='Este país será utilizado para saber el '
                                           'código de marcación correspondiente al número de teléfono').formfield()
    phone = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': '9999999999',
        'class': 'required-field bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    alternative_phone = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': '9999999999',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'johndoe@example.com',
        'class': 'required-field bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    alternative_email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'johndoe123@example.com',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    link_to_classroom = forms.URLField(max_length=300, required=False, widget=forms.URLInput(attrs={
        'placeholder': 'https://example.com',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    code_meeting = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': '00045680?529',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    platform_meeting = forms.ChoiceField(choices=platform_options, required=False, widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    event_planning = forms.FileField(required=True, widget=forms.FileInput(attrs={
        'accept': 'application/pdf, application/vnd.ms-excel',
        'class': 'required-field block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
    }))
    link_video = forms.URLField(max_length=150, required=False, widget=forms.URLInput(attrs={
        'placeholder': 'https://example.com',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'placeholder': 'https://example.com',
        'hidden': 'hidden',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    career = forms.ModelChoiceField(required=False, queryset=Career.objects.all(), widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    teachers = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_teacher=True), required=False, widget=forms.SelectMultiple(attrs={
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

    def clean_alternative_phone(self):
        alt_phone = self.cleaned_data.get('alternative_phone')
        if isinstance(alt_phone, str):
            alt_phone = None
        return alt_phone

    class Meta:
        model = Event
        exclude = ['user', 'date_created', 'active', 'participants']
        help_texts = {
            'country_phone': 'Este país será utilizado para saber el código de marcación correspondiente a número de teléfono',
        }


class ParticipantForm(forms.ModelForm):
    captcha = ReCaptchaField()
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'accept': 'image/jpeg, image/jpg',
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
    }))
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    country_of_birth = CountryField().formfield()
    dni = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    passport_number = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': ' ',
        'value': 0,
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    gender = forms.ChoiceField(choices=gender_options, required=True, widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    current_country = CountryField().formfield()
    address = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Street address',
        'rows': 2,
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    phone = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': ' ',
        'readonly': True,
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    alternative_email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    referral = forms.ModelChoiceField(required=False, empty_label='Nadie', queryset=User.objects.filter(is_referral=True), widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    object = forms.CharField(max_length=256, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'I want to be at the event, because...',
        'rows': 2,
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    how_did_you_find_out = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={
        'placeholder': '¿Cómo nos descubriste?',
        'rows': 2,
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        today = timezone.now()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if age < 15:
            raise ValidationError('Debes tener al menos 15 años de edad.')
        return birthdate

    class Meta:
        model = Participant
        exclude = ['date_created', 'active', 'user', 'event', 'pay']


class ParticipantDataUpdateForm(forms.ModelForm):
    captcha = ReCaptchaField()
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'accept': 'image/jpeg, image/jpg',
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
    }))
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    country_of_birth = CountryField().formfield()
    dni = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    passport_number = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    gender = forms.ChoiceField(choices=gender_options, required=True, widget=forms.Select(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
    }))
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    current_country = CountryField().formfield().widget = forms.Select(attrs={'class': 'Hola'})
    address = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Street address',
        'rows': 2,
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    phone = forms.CharField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': ' ',
        'class': 'rounded-none rounded-r-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    alternative_email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': ' ',
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))
    object = forms.CharField(max_length=256, required=True, widget=forms.Textarea(attrs={
        'placeholder': 'I want to be at the event, because...',
        'rows': 2,
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
    }))

    class Meta:
        model = Participant
        fields = ['profile_image', 'first_name', 'last_name', 'country_of_birth', 'dni', 'passport_number', 'gender',
                  'birthdate', 'current_country', 'address', 'phone', 'email', 'alternative_email', 'object']


class DateInput(forms.DateInput):
    input_type = 'date'
