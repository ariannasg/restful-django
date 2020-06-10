[![CI Workflow](https://github.com/ariannasg/restful-django/workflows/CI%20Workflow/badge.svg)](https://github.com/ariannasg/restful-django/actions?query=workflow%3A%22CI+Workflow%22)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

# RESTful Web APIs with Django - Course

* [Description](#description)
* [Objectives](#objectives)
* [Steps taken to setup the project](#steps-taken-to-setup-the-project)
* [Using the Django shell](#using-the-django-shell)
* [Using curl for testing the API](#using-curl-for-testing-the-api)
* [Beyond the course activities](#beyond-the-course-activities)
* [TODOs](#todos)
* [License](#license)

## Description
Create a simple RESTful web API using Django by following the course https://www.linkedin.com/learning/building-restful-web-apis-with-django.

## Objectives
Practicing Django by:

- Creating a serializer
- Working with API views
- Filtering back ends
- Enabling pagination
- Executing CRUD operations
- Managing serializer fields
- Testing API views

## Steps taken to setup the project
- Copied the existing project from the course resources and cleaned it up
- Created and activated a virtual environment:
    ```
    python3 -m venv ~/.python-envs/restful-django  
    source  ~/.python-envs/restful-django/bin/activate 
    ```
- Upgraded pip and installed project dependencies using the virtualenv:
    ```
    (restful-django) ➜  pip install --upgrade pip   
    (restful-django) ➜  pip install -r requirements.txt 

    ```
- Configured the IDE Interpreter to use the virtual environment as project interpreter
- Checked and applied migrations:
  ```
  (restful-django) ➜  python3 manage.py showmigrations
  (restful-django) ➜  python3 manage.py migrate
  ```
- Created a super user to access the admin site and run the app:
   ```
   (restful-django) ➜ python3 manage.py createsuperuser
   (restful-django) ➜ python3 manage.py runserver
   ```
- Checked http://127.0.0.1:8000/
- Checked http://127.0.0.1:8000/admin using the super user credentials

## Using the Django shell
Example of using the django shell for rapid prototyping of a serializer class:
   
    (restful-django) ➜  demo git:(master) ✗ python3 manage.py shell
    
    Python 3.8.3 (v3.8.3:6f8c8320e9, May 13 2020, 16:29:34) 
    [Clang 6.0 (clang-600.0.57)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from store.models import Product
    >>> product = Product.objects.all()[0]
    >>> product
    <Product object (1) "Mineral Water Strawberry">
    
    >>> from store.serializers import ProductSerializer
    >>> serializer = ProductSerializer()
    >>> data = serializer.to_representation(product)
    >>> data
    OrderedDict([('id', 1), ('name', 'Mineral Water Strawberry'), ('description', 'Natural-flavored strawberry with an anti-oxidant kick.'), ('price', 1.0), ('sale_start', None), ('sale_end', None), ('is_on_sale', False), ('current_price', 1.0)])
    
    >>> from rest_framework.renderers import JSONRenderer
    >>> renderer = JSONRenderer()
    >>> renderer.render(data)
    b'{"id":1,"name":"Mineral Water Strawberry","description":"Natural-flavored strawberry with an anti-oxidant kick.","price":1.0,"sale_start":null,"sale_end":null,"is_on_sale":false,"current_price":1.0}'
    >>> 
 
Another example for using the serializer to show model relationships:
    
    (restful-django) ➜  demo git:(master) ✗ python3 manage.py shell
    
    Python 3.8.3 (v3.8.3:6f8c8320e9, May 13 2020, 16:29:34) 
    [Clang 6.0 (clang-600.0.57)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> import json
    >>> from store.models import *
    >>> from store.serializers import *
    >>> product = Product.objects.all().first()
    >>> cart = ShoppingCart()
    >>> cart.save()
    >>> item = ShoppingCartItem(shopping_cart=cart, product=product, quantity=5)
    >>> item.save()
    >>> serializer = ProductSerializer(product)
    >>> print(json.dumps(serializer.data, indent=2))
    {
      "id": 1,
      "name": "Mineral Water Strawberry",
      "description": "Natural-flavored strawberry with an anti-oxidant kick.",
      "price": 1.0,
      "sale_start": null,
      "sale_end": null,
      "is_on_sale": false,
      "current_price": 1.0,
      "cart_items": [
        {
          "product": 1,
          "quantity": 5
        }
      ]
    }
    >>> 
    
## Using curl for testing the API
    (restful-django) ➜  demo git:(master) curl -X POST http://127.0.0.1:8000/api/v1/products/new -d price=1.00 -d name="product to delete" -d description="this is a test"
    {"id":7,"name":"product to delete","description":"this is a test","price":1.0,"sale_start":null,"sale_end":null,"is_on_sale":false,"current_price":1.0}%                                             
    
    (restful-django) ➜  demo git:(master) curl -X DELETE http://127.0.0.1:8000/api/v1/products/7/destroy


## Beyond the course activities
Things that I added/modified which weren't part of the course:

- Upgraded version of packages used
- Installed deps and changed config to use PostgreSQL instead of SQLite
- Installed safety and pylint for running security checks and linting
- Created a config file for pylint and added some extra setup
- Created a makefile with the basic commands to run locally and during CI/CD
- Configured a test database
- Configured a CI workflow for using github-actions
- Installed the coverage package, created a config file for it and and added commands to the makefile for generating test coverage
- Configured project to use pipenv
- Configured project to use mypy for type checking

## TODOs
Please see list of [TODOs](TODO.md).
  
## License
This project is licensed under the terms of the MIT License.
Please see [LICENSE](LICENSE.md) for details.
