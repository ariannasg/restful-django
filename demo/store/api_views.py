#!usr/bin/env python3
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from store.models import Product
from store.serializers import ProductSerializer


# The generic views in Django REST framework will cover what you need from a
# REST API in many cases. This is an example of a list API view
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # we add the ability to filter products using URL query parameters
    filter_backends = (DjangoFilterBackend,)
    # we are going to filter products by whether they match a specific ID
    filter_fields = ('id', )

    # we are also to filter products by whether they are on sale or not
    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()  # don't do anything

        queryset = Product.objects.all()
        if on_sale.lower() == 'true':
            now = timezone.now()
            return queryset.filter(sale_start__lte=now, sale_end__gte=now)

        return queryset
