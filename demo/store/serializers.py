from rest_framework import serializers

from store.models import Product, ShoppingCartItem


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    # to simplify how we added custom field data, we can make the attributes
    # that we initially set in the two representation method, to use serializer
    # fields.
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    # override the description field by adding some props to it for adding
    # validation
    description = serializers.CharField(min_length=2, max_length=100)
    # The SerializerMethodField will by default call the method get_cart_items
    # For other fields, it will use the Get "underscore" as a prefix to the
    # field name.
    cart_items = serializers.SerializerMethodField()
    # thanks to this we could delete the validation on the creation api view.
    # this validation will be applied on the update too
    price = serializers.DecimalField(min_value=1.0, max_value=100000,
                                     max_digits=None, decimal_places=2)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price',
                  'sale_start', 'sale_end', 'is_on_sale', 'current_price',
                  'cart_items')

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        # the "many" parameter is used to control whether one cart item is
        # serialized or whether a list serializer is automatically created
        # to serialize a collection of cart items.
        return CartItemSerializer(items, many=True).data
