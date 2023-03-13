from django.shortcuts import render
from Apps.Eventos.models import EventParticipant
from Apps.Eventos.forms import EventParticipantForm


def eventos(request):
    data = {
        'form': EventParticipantForm
    }
    return render(request, 'Eventos/index.html', data)
