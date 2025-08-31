from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        """
        Imports signals when the app is ready to ensure they are connected.
        """
        import properties.signals # noqa: F401
