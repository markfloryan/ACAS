from django.apps import AppConfig

class SptAppConfig(AppConfig):
    name = 'sptApp'

    def ready(self):
        import sptApp.signals