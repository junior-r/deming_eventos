from django.urls import path

from Apps.Eventos.views import view_events, careers, view_event, send_whatsapp_event, send_email_event, \
    set_active_participant, pago, download_certify_event

urlpatterns = [
    path('', view_events, name='eventos'),
    path('careers/', careers, name='careers'),
    path('pago/<int:id_event>/', pago, name='pago'),
    path('view_event/<int:id_event>/', view_event, name='view_event'),
    path('send_email_event/<int:id_event>/<str:template_route>/', send_email_event, name='send_email_event'),
    path('send_whatsapp_event/<int:id_event>/', send_whatsapp_event, name='send_whatsapp_event'),
    path('set_active_participant/<int:id_event>/', set_active_participant, name='set_active_participant'),
    path('download_certify_event/<int:id_event>/<int:id_participant>/', download_certify_event,
         name='download_certify_event'),
]
