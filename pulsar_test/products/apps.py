from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    name = 'pulsar_test.products'
    verbose_name = _('Продукты')

    def ready(self):
        import pulsar_test.products.signals
