#!usr/bin/env python3
from rest_framework.generics import ListAPIView

from store.models import Product
from store.serializers import ProductSerializer


# The generic views in Django REST framework will cover what you need from a
# REST API in many cases. This is an example of a list API view
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
