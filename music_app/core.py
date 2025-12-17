from django.apps import AppConfig


class MusicAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "music_app"

    def ready(self):
        import music_app.models
