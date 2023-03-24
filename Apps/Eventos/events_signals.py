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
        if now < instance.start_date or now > instance.final_date:
            if instance.active is True:
                instance.active = False
                instance.save()
        else:
            if instance.active is False:
                instance.active = True
                instance.save()
