from django.urls import path

from Apps.Eventos.views import view_events, careers, view_event, update_event, send_whatsapp_event, send_email_event, \
    set_active_participant, pago, download_certify_event, update_career, delete_career, create_career_ajax, \
    download_invoice, delete_event

urlpatterns = [
    path('', view_events, name='eventos'),
    path('careers/', careers, name='careers'),
    path('create_career_ajax/', create_career_ajax, name='create_career_ajax'),
    path('edit_career/<int:id_career>/', update_career, name='update_career'),
    path('delete_career/<int:id_career>/', delete_career, name='delete_career'),
    path('pago/<int:id_event>/', pago, name='pago'),
    path('view_event/<int:id_event>/', view_event, name='view_event'),
    path('update_event/<int:id_event>/', update_event, name='update_event'),
    path('delete_event/<int:id_event>/', delete_event, name='delete_event'),
    path('download_invoice/<int:id_event>/', download_invoice, name='download_invoice'),
    path('send_email_event/<int:id_event>/<str:template_route>/', send_email_event, name='send_email_event'),
    path('send_whatsapp_event/<int:id_event>/', send_whatsapp_event, name='send_whatsapp_event'),
    path('set_active_participant/<int:id_event>/', set_active_participant, name='set_active_participant'),
    path('download_certify_event/<int:id_event>/<int:id_participant>/', download_certify_event,
         name='download_certify_event'),
]
