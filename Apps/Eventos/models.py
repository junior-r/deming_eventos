import os
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django_countries.fields import CountryField
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


gender_options = [
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
]


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
    curriculum = models.FileField(upload_to=participant_directory_file_path, validators=[FileExtensionValidator(['pdf'])], blank=False, null=False)
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
