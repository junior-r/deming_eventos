import os
from datetime import datetime

import phonenumbers
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from django.urls import reverse

from Apps.Users.models import User


def participant_directory_image_path(instance, filename):
    profile_image_name = 'Events/Participants/Images/{0}/profile.jpg'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_image_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_image_name


def participant_directory_file_path(instance, filename):
    file_name = 'Events/Participants/Docs/{0}/curriculum.pdf'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_name


def event_directory_user_file_path(instance, filename):
    file_name = 'Events/Events/PersonInChange/Docs/{0}/{1}'.format(instance, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_name


def event_directory_planning_file_path(instance, filename):
    file_name = 'Events/Events/Planning/Docs/{0}/{1}'.format(instance, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_name


def event_directory_logo_path(instance, filename):
    file_name = 'Events/Events/Logos/{0}/logo.jpg'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_name


gender_options = [
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
]


class Career(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, unique=True,
                            error_messages={'unique': 'Ya existe un registro con este nombre. Intente con otro.'})
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}'.format(self.name)


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=participant_directory_image_path, blank=True, null=True,
                                      default="user_profile_placeholder.jpg")
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    country_of_birth = CountryField(blank=False, null=False)
    dni = models.BigIntegerField(unique=True, blank=False, null=False, error_messages={
        'unique': 'Ya exíste un participante con este número de identificación',
    })
    passport_number = models.BigIntegerField(unique=True, blank=True, null=True, error_messages={
        'unique': 'Ya exíste un participante con este pasaporte',
    })
    gender = models.CharField(max_length=15, choices=gender_options, blank=False, null=False)
    birthdate = models.DateField(blank=False, null=False)
    current_country = CountryField(blank=False, null=False)
    address = models.TextField(max_length=400, blank=False, null=False)
    phone = models.BigIntegerField(blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False, error_messages={
        'unique': 'Ya esxite un participante con este email',
    })
    alternative_email = models.EmailField(unique=True, blank=True, null=True, error_messages={
        'unique': 'Ya esxite un participante con este email alternativo',
    })
    object = models.TextField(max_length=256, blank=False, null=False)
    how_did_you_find_out = models.TextField(max_length=256, blank=True, null=True, default='')
    referral = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=False, related_name='referral')
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Participants'

    def __str__(self):
        return '{0}_{1}'.format(self.first_name, self.dni)

    def get_profile_image(self) -> object:
        if self.profile_image:
            return '{}'.format(os.path.join('/media/', self.profile_image.name))
        else:
            return '{}{}'.format(settings.MEDIA_URL, 'user_profile_placeholder.jpg')

    def get_age(self):
        birthdate = self.birthdate.__str__()
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def get_full_number_phone(self):
        try:
            phone_number_info = phonenumbers.parse(f'{self.phone}', self.current_country.__str__())
            return '+{0}{1}'.format(phone_number_info.country_code, phone_number_info.national_number)
        except phonenumbers.NumberParseException:
            return None

    def get_inter_dialling_code(self):
        try:
            phone_number_info = phonenumbers.parse(f'{self.phone}', self.current_country.__str__())
            return '+{}'.format(phone_number_info.country_code)
        except phonenumbers.NumberParseException:
            return None

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_passport_number(self):
        if self.passport_number != 0:
            return self.passport_number
        return '-'

    def delete(self, *args, **kwargs):
        try:
            if self.profile_image:
                os.remove(self.profile_image.path)
                self.profile_image.delete(False)
        except ValueError:
            pass
        except WindowsError:
            pass
        finally:
            super(Participant, self).delete(*args, **kwargs)


class Event(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    participants = models.ManyToManyField(Participant, through='EventParticipant')
    logo = models.ImageField(upload_to=event_directory_logo_path, blank=True, null=True,
                             validators=[FileExtensionValidator(['jpeg', 'jpg'])])
    title = models.CharField(max_length=150, null=False, blank=False, unique=True)
    place = models.CharField(max_length=150, null=False, blank=False)
    addressed_to = models.TextField(max_length=300, null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateField(null=False, blank=False)
    final_date = models.DateField(null=False, blank=False)
    modality = models.CharField(max_length=20, choices=modality_options, blank=False, null=False)
    country_phone = CountryField(blank=False, null=False)
    phone = models.BigIntegerField(null=False, blank=False)
    alternative_phone = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(unique=False, null=False, blank=False)
    alternative_email = models.EmailField(unique=False, null=True, blank=True)
    link_to_classroom = models.URLField(null=True, blank=False)
    code_meeting = models.CharField(max_length=500, null=True, blank=False)
    platform_meeting = models.CharField(null=True, blank=False, choices=platform_options, max_length=20)
    event_planning = models.FileField(upload_to=event_directory_planning_file_path, max_length=255,
                                      validators=[FileExtensionValidator(['pdf'])], blank=False, null=False)
    link_video = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    certify = models.BooleanField(default=False)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=False)
    teachers = models.ManyToManyField(User, related_name='teachers', blank=True)
    url = models.URLField(blank=False, null=False)

    def get_full_number_phone(self):
        try:
            phone_number_info = phonenumbers.parse(f'{self.phone}', self.country_phone.__str__())
            return '+{0}{1}'.format(phone_number_info.country_code, phone_number_info.national_number)
        except phonenumbers.NumberParseException:
            return None

    def get_inter_dialling_code(self):
        try:
            phone_number_info = phonenumbers.parse(f'{self.phone}', self.country_phone.__str__())
            return '+{}'.format(phone_number_info.country_code)
        except phonenumbers.NumberParseException:
            return None

    def get_logo(self) -> object:
        if self.logo:
            logo_root = os.path.join(settings.MEDIA_URL, f'{self.logo}')
            return '{}'.format(logo_root)
        else:
            return '{}{}'.format(settings.MEDIA_URL, 'event_image_placeholder.png')

    def get_planning_event(self) -> object:
        if self.event_planning:
            return '{}{}'.format(settings.MEDIA_URL, self.event_planning)
        else:
            return None

    def get_short_name(self):
        if len(self.title) > 12:
            return self.title[:12] + '...'
        return self.title

    def get_absolute_url(self):
        return reverse('view_event', kwargs={'id_event': self.id})

    def get_unicode(self):
        if len(self.title) > 8:
            return '{0}-{1}_{2}_{3}_{4}'.format(self.id, self.title[:8], self.start_date.year, self.start_date.month,
                                                self.start_date.day)
        else:
            return '{0}-{1}_{2}_{3}_{4}'.format(self.id, self.title, self.start_date.year, self.start_date.month,
                                                self.start_date.day)

    def delete(self, *args, **kwargs):
        try:
            if self.logo:
                os.remove(self.logo.path)
                self.logo.delete(False)

            os.remove(self.event_planning.path)
            self.event_planning.delete(False)
        except ValueError:
            pass
        except WindowsError:
            pass
        except:
            pass
        finally:
            super(Event, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'Events'
        ordering = ['start_date']

    def __str__(self):
        return '{}_{}_to_{}'.format(self.title, self.start_date, self.final_date)


class EventParticipant(models.Model):
    order_id = models.CharField(unique=True, max_length=100, editable=False, null=True, blank=True)
    capture_id = models.CharField(unique=True, max_length=100, editable=False, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    participant = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True)
    client_name = models.CharField(max_length=150, null=True)
    client_email = models.EmailField(blank=True, null=True)
    payer_id = models.CharField(max_length=100, editable=False, null=True, blank=True)
    active = models.BooleanField(default=False)
    total_buy = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_paypal = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    net_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status_buy = models.CharField(max_length=15, default='')
    status_code = models.CharField(max_length=100, default='')
    pay = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def get_active_state(self):
        if self.active:
            return '<svg fill="none" class="w-6 h-6 mr-2 -ml-1" stroke="green" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"> <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path> </svg>'
        else:
            return '<svg fill="none" class="w-6 h-6 mr-2 -ml-1" stroke="red" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"> <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path> </svg>'

    class Meta:
        db_table = 'EventParticipants'

    def __str__(self):
        return '{}'.format(self.id)
