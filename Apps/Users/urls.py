from django.urls import path, include
from Apps.Users.views import sign_up


urlpatterns = [
    path('sing_up/', sign_up, name='sign_up'),
]
