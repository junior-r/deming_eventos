from django.apps import AppConfig


class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apps.Eventos'

    def ready(self):
        from Apps.Eventos import events_signals
