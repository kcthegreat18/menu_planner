from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Import here to avoid early model access before apps are ready
        from .scheduler import start_scheduler
        start_scheduler()
