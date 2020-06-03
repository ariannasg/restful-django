import os
from unittest import skip

from django.conf import settings
from rest_framework.test import APITestCase

from store.models import Product


class ProductDestroyTestCase(APITestCase):
    # TODO: ideally we'll also test that the cache doesn't longer exist
    def test_delete_product(self):
        initial_product_count = Product.objects.count()
        product_id = Product.objects.first().id
        self.client.delete('/api/v1/products/{}/'.format(product_id))
        self.assertEqual(
            Product.objects.count(),
            initial_product_count - 1,
        )
        self.assertRaises(
            Product.DoesNotExist,
            Product.objects.get, id=product_id,
        )


class ProductListTestCase(APITestCase):
    def test_list_products(self):
        products_count = Product.objects.count()
        response = self.client.get('/api/v1/products/')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], products_count)
        self.assertEqual(len(response.data['results']), products_count)


class ProductUpdateTestCase(APITestCase):
    def test_update_product(self):
        product = Product.objects.first()
        response = self.client.patch(
            '/api/v1/products/{}/'.format(product.id),
            {
                'name': 'New Product',
                'description': 'Awesome product',
                'price': 123.45,
            },
            format='json',
        )
        updated = Product.objects.get(id=product.id)
        self.assertEqual(updated.name, 'New Product')

    def test_upload_product_photo(self):
        product = Product.objects.first()
        original_photo = product.photo
        photo_path = os.path.join(settings.MEDIA_ROOT, 'products',
                                  'vitamin-iron.jpg')

        # REST APIs usually use JSON objects, however images and files are
        # binary data and so the multipart format is used to parse that data.
        with open(photo_path, 'rb') as photo_data:
            response = self.client.patch(
                '/api/v1/products/{}/'.format(product.id), {
                    'photo': photo_data,
                }, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['photo'], original_photo)
        try:
            updated = Product.objects.get(id=product.id)
            expected_photo = os.path.join(settings.MEDIA_ROOT, 'products',
                                          'vitamin-iron')
            self.assertTrue(updated.photo.path.startswith(expected_photo))
        finally:
            os.remove(updated.photo.path)


class ProductCreateTestCase(APITestCase):
    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            'name': 'New Product',
            'description': 'Awesome product',
            'price': '123.45',
        }
        response = self.client.post('/api/v1/products/new', product_attrs)
        print(response.data)

        if response.status_code != 201:
            print(response.data)

        # check the product count
        self.assertEqual(
            Product.objects.count(),
            initial_product_count + 1,
        )

        # check the values  for the prod were set correctly
        for attr, expected_value in product_attrs.items():
            self.assertEqual(response.data[attr], expected_value)

        # check the custom fields were set correctly
        self.assertEqual(response.data['is_on_sale'], False)
        self.assertEqual(
            response.data['current_price'],
            float(product_attrs['price']),
        )
