from django.apps import AppConfig


class BonusesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bonuses'

    def ready(self):
        import Bonuses.signals
