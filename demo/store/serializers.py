from rest_framework import serializers

from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    # to simplify how we added custom field data, we can make the attributes
    # that we initially set in the two representation method, to use serializer
    # fields.
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    # override the description field by adding some props to it for adding
    # validation
    description = serializers.CharField(min_length=2, max_length=100)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price',
                  'sale_start', 'sale_end', 'is_on_sale', 'current_price')
