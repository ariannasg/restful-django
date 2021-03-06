#!usr/bin/env python3
from django.core.cache import cache
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from store.models import Product
from store.serializers import ProductSerializer, ProductStatsSerializer


# Page number and limit offset pagination are good for small- to medium-sized
# data sets. However, only cursor pagination (which uses the databases cursor)
# is efficient enough for large data sets.
class ProductsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


# The generic views in Django REST framework will cover what you need from a
# REST API in many cases. This is an example of a list API view
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # we add the ability to filter products using URL query parameters
    filter_backends = (DjangoFilterBackend, SearchFilter)
    # this is used by the DjangoFilterBackend to filter products by ID
    filter_fields = ('id',)
    # this is used by the SearchFilter backend to map from the URL query
    # parameters, to the model fields of the serialized model
    search_fields = ('name', 'description')
    # using offset pagination
    # now the api result will include things like:
    #   "count": 4,
    #   "next": "http://127.0.0.1:8000/api/v1/products?limit=1&offset=2",
    #   "previous": "http://127.0.0.1:8000/api/v1/products?limit=1",
    #   "results": [ ... ]
    pagination_class = ProductsPagination

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


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        # add the validation of the price for avoiding creating free products
        price = self.request.data.get('price')
        try:
            if price is not None and float(price) <= 0.0:
                # The ValidationError exception can be raised with a
                # field mapping using a dict
                raise ValidationError({'price': 'must be above $0.0'})
        except ValueError:
            raise ValidationError({'price': 'must to be a number'})

        return super().create(request, *args, **kwargs)


# The generic RetrieveUpdateDestroyAPIView combines the “get”, “put”, “patch”,
# and “delete” HTTP methods into one API view.
class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    # in a real-world scenario we'll prob need to clear all the cache
    # linked to this product that's being destroyed
    def delete(self, request, *args, **kwargs):
        product_id = self.request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        # if object was deleted successfully, remove all associated cache
        if response.status_code == 204:
            cache.delete(f'product_data_{product_id}')
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            product = response.data
            cache.set(f"product_data_{product['id']}", {
                'name': product['name'],
                'description': product['description'],
                'price': product['price']
            })
        return response


# Composite fields are highly useful when you're trying to return
# data that needs to be structured in a specific way that may not map to any
# model.
class ProductStats(GenericAPIView):
    lookup_field = 'id'
    serializer_class = ProductStatsSerializer
    queryset = Product.objects.all()

    def get(self, request, format=None, id=None):
        obj = self.get_object()
        serializer = ProductStatsSerializer({
            'stats': {
                '2019-01-01': [5, 10, 15],
                '2019-01-02': [20, 1, 1]
            }
        })
        return Response(serializer.data)
