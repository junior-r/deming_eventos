from django.contrib import admin
from Apps.Eventos.models import Career, Participant, Event, EventParticipant
from Apps.Eventos.forms import EventForm


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'start_date', 'final_date', 'phone', 'email')
    form = EventForm


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'capture_id', 'event', 'participant', 'payer_id', 'client_name', 'client_email', 'active', 'pay', 'total_buy', 'status_buy', 'date_created')


admin.site.register(Career)
admin.site.register(Participant)

admin.site.register(Event, EventAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
