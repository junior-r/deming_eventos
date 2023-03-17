from django.contrib import admin
from Apps.Eventos.models import Career, Participant, Event, EventParticipant


admin.site.register(Career)
admin.site.register(Participant)
admin.site.register(Event)
admin.site.register(EventParticipant)

# Register your models here.
