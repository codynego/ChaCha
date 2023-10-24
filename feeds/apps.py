from django.apps import AppConfig

class FeedsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feeds'

    def ready(self):
        import feeds.signals # Import your app's models.py

