from django.urls import path, include
from Apps.Eventos.views import eventos


urlpatterns = [
    path('', eventos, name='eventos'),
]
