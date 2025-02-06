from django.apps import AppConfig

class ProductsConfig(AppConfig):
    name = 'products'

    def ready(self):
        import products.signals  # Import the signals module to connect the signal