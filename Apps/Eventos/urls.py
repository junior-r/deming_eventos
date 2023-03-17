from django.urls import path

from Apps.Eventos.views import view_events, careers, view_event, send_whatsapp_event, paypal_return, paypal_cancel, \
    send_email_event, set_active_participant

urlpatterns = [
    path('', view_events, name='eventos'),
    path('careers/', careers, name='careers'),
    path('view_event/<int:id_event>/', view_event, name='view_event'),
    path('send_email_event/<int:id_event>/<str:template_route>/', send_email_event, name='send_email_event'),
    path('send_whatsapp_event/<int:id_event>/', send_whatsapp_event, name='send_whatsapp_event'),
    path('paypal_return/<int:id_event>/', paypal_return, name='paypal_return'),
    path('paypal_cancel/<int:id_event>/', paypal_cancel, name='paypal_cancel'),
    path('set_active_participant/<int:id_participant>/<int:id_event>/', set_active_participant, name='set_active_participant'),
]
