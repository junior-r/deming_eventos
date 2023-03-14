from django.urls import path, include
from Apps.Eventos.views import events, careers


urlpatterns = [
    path('', events, name='eventos'),
    path('careers/', careers, name='careers'),
]
