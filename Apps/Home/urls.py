from django.urls import path, include
from Apps.Home.views import index, privacy_policy, terms_and_conditions


urlpatterns = [
    path('', index, name='index'),
    path('Privacy-Policy/', privacy_policy, name='privacy_policy'),
    path('Terms_&_Conditions/', terms_and_conditions, name='terms_and_conditions'),
]
