from django.apps import AppConfig

class OrdersConfig(AppConfig):
    name = 'orders'

    def ready(self):
        from . import signals  # Use a relative import to import the signals module