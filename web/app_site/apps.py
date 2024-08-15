from django.apps import AppConfig


class AppSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_site'
    verbose_name = 'Order accounting system'

    def ready(self):
        import app_site.signals
