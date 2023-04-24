import datetime

from django.db.models.signals import post_init, post_save, pre_save
from django.dispatch import receiver
from Apps.Eventos.models import Event
from django.utils import timezone


@receiver(post_init, sender=Event)
@receiver(pre_save, sender=Event)
@receiver(post_save, sender=Event)
def update_active_signal(sender, instance, **kwargs):
    now = timezone.now().date()
    if instance.start_date is not None and instance.final_date is not None:
        start_date = datetime.datetime.strptime(str(instance.start_date), '%Y-%m-%d').date()
        final_date = datetime.datetime.strptime(str(instance.final_date), '%Y-%m-%d').date()
        status_certify = instance.certify
        if now > start_date:
            if instance.active is True:
                instance.active = False
                instance.save()
            if now > final_date:
                if instance.certify is False:
                    instance.certify = True
                    instance.save()
