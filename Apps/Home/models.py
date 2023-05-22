from django.db import models
from django_countries.fields import CountryField


class EmailContact(models.Model):
    subject = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.CharField(max_length=700, null=False, blank=False)

    def __str__(self):
        return self.email


class EmailContactEvent(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return self.email


class WhatsAppContact(models.Model):
    names = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    country = CountryField(blank=False, null=False)
    phone = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.phone)
