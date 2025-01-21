from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self, *args, **kwargs):
        import home.signals  # noqa

        super_ready = super().ready(*args, **kwargs)

        return super_ready
