from django.apps import AppConfig


class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apps.Eventos'

    def ready(self):
        import Apps.Eventos.signals
