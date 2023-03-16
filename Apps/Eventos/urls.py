from django.urls import path, include
from Apps.Eventos.views import view_events, careers, view_event, send_whatsapp_event


urlpatterns = [
    path('', view_events, name='eventos'),
    path('careers/', careers, name='careers'),
    path('view_event/<int:id_event>/', view_event, name='view_event'),
    path('send_whatsapp_event/<int:id_event>/', send_whatsapp_event, name='send_whatsapp_event'),
]
