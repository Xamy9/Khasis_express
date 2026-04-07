from django.apps import AppConfig
import os

class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services'

    def ready(self):
        # Prevent multiple executions
        if os.environ.get("RUN_MAIN") == "true":
            from .create_superuser import create_superuser
            create_superuser()