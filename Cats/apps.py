from django.apps import AppConfig


class CatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cats'

    def ready(self):
        import Cats.signals
