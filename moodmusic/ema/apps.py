from django.apps import AppConfig


class EmaConfig(AppConfig):
    name = "moodmusic.ema"

    def ready(self):
        import moodmusic.ema.signals  # noqa
