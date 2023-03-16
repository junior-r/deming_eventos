from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from Apps.Eventos.models import EventParticipant
from django.dispatch import receiver


@receiver(valid_ipn_received)
def valid_inp_signal(sender, **kwargs):
    print('Payment Valid')
    ipn = sender
    if ipn.payment_status == 'Completed':
        pass


@receiver(invalid_ipn_received)
def invalid_inp_signal(sender, **kwargs):
    print('Payment Invalid')
    ipn = sender
    if ipn.payment_status == 'Completed':
        pass

