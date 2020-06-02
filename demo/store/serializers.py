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
    # The output format is set to none so that the fields are always DateTime
    # objects. required false will allow not setting them on creation
    sale_start = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2019'})
    sale_end = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2019'})
    photo = serializers.ImageField(default=None)
    # We're going to allow the uploading of a warranty file for a product.
    # We use the file field for this, but since the product model does not
    # have a warranty file field in the model itself, we're going to be adding
    # the write-only configuration option. This means that when we write to
    # the field the data does not get saved to the model.
    # We're going to override the update method, so that we can make use of
    # the warranty field. If a warranty file is supplied,
    # we're going to add it to the description of the product.
    # we can use write-only fields when a field is being written to and
    # the data can be used in other model fields.
    warranty = serializers.FileField(write_only=True, default=None)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price',
                  'sale_start', 'sale_end', 'is_on_sale', 'current_price',
                  'cart_items', 'photo', 'warranty')

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        # the "many" parameter is used to control whether one cart item is
        # serialized or whether a list serializer is automatically created
        # to serialize a collection of cart items.
        return CartItemSerializer(items, many=True).data

    # Validated data in the update method is the data that will be used to
    # update the model. It is safe to access because it is already passed
    # through the validation process.
    def update(self, instance, validated_data):
        if validated_data.get('warranty', None):
            instance.description += '\n\nWarranty Information:\n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode()
        return super().update(instance, validated_data)

    # implement this method so we don't get the following error when testing
    # the creation of a product:
    # TypeError: Product() got an unexpected keyword argument 'warranty'
    def create(self, validated_data):
        validated_data.pop('warranty')
        return super().create(validated_data)


# In order to gather daily, weekly, or monthly product and shopping cart data
# for our sales report, we need to create a new serializer that uses composite
# fields. This won't be a model serializer but just a plain serializer.
class ProductStatsSerializer(serializers.Serializer):
    # this is a composite of a composite field
    stats = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField()
        )
    )
