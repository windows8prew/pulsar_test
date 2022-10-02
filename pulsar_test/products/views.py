from rest_framework import viewsets, permissions, filters
from filters.mixins import FiltersMixin

from pulsar_test.products.models import Product
from pulsar_test.products.serializers import ProductSerializer
from pulsar_test.products.validations import product_query_schema


class ProductViewSet(FiltersMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('get',)
    filter_backends = (filters.OrderingFilter,)

    filter_mappings = {
        'status': 'status',
        'article': 'article',
        'name': 'name',
    }

    filter_validation_schema = product_query_schema
