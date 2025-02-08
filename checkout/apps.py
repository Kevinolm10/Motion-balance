from django.apps import AppConfig

class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        from . import signals  # Use a relative import to import the signals module