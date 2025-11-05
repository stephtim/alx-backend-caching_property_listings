from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        # Import signal handlers to connect them. Placing import here
        # ensures the app registry is ready and avoids import-time side effects.
        from . import signals  # noqa: F401
