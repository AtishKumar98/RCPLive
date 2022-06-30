from django.apps import AppConfig


class EcartproductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EcartProducts'

    
    def ready(self):
        import EcartProducts.signals