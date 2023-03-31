import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_image_path(instance, filename):
    profile_image_name = 'Users/Images/{0}/profile.jpg'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_image_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_image_name


class User(AbstractUser):
    profile_image_user = models.ImageField(upload_to=user_directory_image_path, blank=True, null=True,
                                           default="user_profile_placeholder.jpg")

    def delete(self, *args, **kwargs):
        try:
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
        if self.is_superuser:
            return '<span class="bg-yellow-100 text-yellow-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300">Superusuario</span>'
        elif self.is_staff:
            return '<span class="bg-green-100 text-green-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300">Staff</span>'
        else:
            return '<span class="bg-purple-100 text-purple-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-purple-900 dark:text-purple-300">Usuario</span>'

    def get_picture_profile(self):
        if self.profile_image_user:
            return '{}'.format(os.path.join(settings.MEDIA_URL, self.profile_image_user.url))
        else:
            return '{}{}'.format(settings.MEDIA_URL, 'user_profile_placeholder.jpg')

    def __str__(self):
        return self.username
