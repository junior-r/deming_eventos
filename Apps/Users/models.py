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

    def get_picture_profile(self):
        if self.profile_image_user:
            return '{}'.format(os.path.join(settings.MEDIA_URL, self.profile_image_user.url))
        else:
            return '{}{}'.format(settings.MEDIA_URL, 'user_profile_placeholder.jpg')

    def save(self, *args, **kwargs):
        user = super(User, self)
        user.set_password(self.password)
        user.save(*args, **kwargs)
        return user

    def __str__(self):
        return self.username
