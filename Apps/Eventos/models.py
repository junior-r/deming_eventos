import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django_countries.fields import CountryField
from Apps.Users.models import User
from django.utils import timezone
import phonenumbers


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
    file_name = 'Events/Events/PersonInChange/Docs/{0}/curriculum.pdf'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_name


def event_directory_planning_file_path(instance, filename):
    file_name = 'Events/Events/Planning/Docs/{0}/planning.pdf'.format(instance)
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


class Event(models.Model):
    modality_options = [
        ('Presencial', 'Presencial'),
        ('Online', 'Online'),
        ('Online y Presencial', 'Online y Presencial'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
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
    curriculum_user = models.FileField(upload_to=event_directory_user_file_path,
                                       validators=[FileExtensionValidator(['pdf'])], blank=False, null=False)
    event_planning = models.FileField(upload_to=event_directory_planning_file_path,
                                      validators=[FileExtensionValidator(['pdf'])], blank=False, null=False)
    link_video = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=False)

    def get_full_number_phone(self):
        phone_number_info = phonenumbers.parse(f'{self.phone}', self.country_phone.__str__())
        return '+{0}{1}'.format(phone_number_info.country_code, phone_number_info.national_number)

    def get_inter_dialling_code(self):
        phone_number_info = phonenumbers.parse(f'{self.phone}', self.country_phone.__str__())
        return '+{}'.format(phone_number_info.country_code)

    def get_logo(self) -> object:
        if self.logo:
            return '{}{}'.format(settings.MEDIA_URL, self.logo)
        else:
            return None

    def delete(self, *args, **kwargs):
        try:
            if self.logo:
                os.remove(self.logo.path)
                self.logo.delete(False)
            os.remove(self.curriculum_user.path)
            self.curriculum_user.delete(False)

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


    def __str__(self):
        return '{}_{}_to_{}'.format(self.title, self.start_date, self.final_date)


class EventParticipant(models.Model):
    profile_image = models.ImageField(upload_to=participant_directory_image_path, blank=True, null=True,
                                      default="user_profile_placeholder.jpg")
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    country_of_birth = CountryField(blank=False, null=False)
    dni = models.BigIntegerField(blank=False, null=False)
    passport_number = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=15, choices=gender_options, blank=False, null=False)
    birthdate = models.DateField(blank=False, null=False)
    current_country = CountryField(blank=False, null=False)
    address = models.TextField(max_length=400, blank=False, null=False)
    phone = models.BigIntegerField(blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    alternative_email = models.EmailField(unique=True, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=False, null=False)
    curriculum = models.FileField(upload_to=participant_directory_file_path,
                                  validators=[FileExtensionValidator(['pdf'])], blank=False, null=False)
    object = models.TextField(max_length=256, blank=False, null=False)
    date_created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{0}_{1}'.format(self.first_name, self.dni)

    def get_full_number_phone(self):
        phone_number_info = phonenumbers.parse(f'{self.phone}', self.current_country.__str__())
        return '+{0}{1}'.format(phone_number_info.country_code, phone_number_info.national_number)

    def get_inter_dialling_code(self):
        phone_number_info = phonenumbers.parse(f'{self.phone}', self.current_country.__str__())
        return '+{}'.format(phone_number_info.country_code)

    def delete(self, *args, **kwargs):
        try:
            if self.curriculum:
                os.remove(self.curriculum.path)
                self.curriculum.delete(False)

            if self.profile_image:
                os.remove(self.profile_image.path)
                self.profile_image.delete(False)
        except ValueError:
            pass
        except WindowsError:
            pass
        finally:
            super(EventParticipant, self).delete(*args, **kwargs)
