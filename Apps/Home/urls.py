from django.urls import path, include
from Apps.Home.views import index


urlpatterns = [
    path('', index, name='index'),
]
