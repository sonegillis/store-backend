from django.apps import AppConfig


class LandingConfig(AppConfig):
    name = 'landing'

    def ready(self):
        import landing.signals
