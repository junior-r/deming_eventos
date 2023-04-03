import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


def user_directory_image_path(instance, filename):
    profile_image_name = 'Users/Images/{0}/profile.jpg'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_image_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_image_name


def user_directory_file_path(instance, filename):
    file_name = 'Users/Docs/{0}/curriculum.pdf'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return file_name


class User(AbstractUser):
    profile_image_user = models.ImageField(upload_to=user_directory_image_path, blank=True, null=True,
                                           default="user_profile_placeholder.jpg")
    is_teacher = models.BooleanField(default=False)
    curriculum = models.FileField(upload_to=user_directory_file_path,
                                  validators=[FileExtensionValidator(['pdf'])], blank=False, null=False)
    profession = models.CharField(max_length=100, blank=False, null=False)

    def delete(self, *args, **kwargs):
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, 'Users', 'Docs', self.__str__(), 'curriculum.pdf'))
            if self.profile_image_user != 'user_profile_placeholder.jpg':
                os.remove(self.profile_image_user.path)
                self.profile_image_user.delete(False)
        except ValueError:
            pass
        except WindowsError:
            pass
        finally:
            super(User, self).delete(*args, **kwargs)

    def get_full_name(self):
        first_name = self.first_name
        last_name = self.last_name
        if first_name and last_name:
            return '{0} {1}'.format(first_name, last_name)
        return self.username

    def get_role(self):
        badge_superuser = '<span class="bg-yellow-300 text-yellow-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300">Superusuario</span>'
        badge_staff = '<span class="bg-green-300 text-green-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300">Staff</span>'
        badge_teacher = '<span class="bg-pink-300 text-pink-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-pink-900 dark:text-pink-300">Profesor</span>'
        badge_user = '<span class="bg-purple-300 text-purple-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-purple-900 dark:text-purple-300">Usuario</span>'
        if self.is_superuser:
            return '{0} {1}'.format(badge_superuser, badge_staff)
        elif self.is_staff and self.is_teacher:
            return '{0} {1}'.format(badge_staff, badge_teacher)
        elif self.is_staff and not self.is_teacher:
            return badge_staff
        elif self.is_teacher:
            return badge_teacher
        else:
            return badge_user

    def get_picture_profile(self):
        if self.profile_image_user:
            return '{}'.format(os.path.join(settings.MEDIA_URL, self.profile_image_user.url))
        else:
            return '{}{}'.format(settings.MEDIA_URL, 'user_profile_placeholder.jpg')

    def get_curriculum(self):
        return '{}'.format(os.path.join(settings.MEDIA_URL, self.curriculum.url))

    def __str__(self):
        return self.username.capitalize()
