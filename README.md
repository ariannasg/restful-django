[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

# RESTful Web APIs with Django - Course

* [Description](#description)
* [Objectives](#objectives)
* [Steps taken to setup the project](#steps-taken-to-setup-the-project)
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
  
## License
This project is licensed under the terms of the MIT License.
Please see [LICENSE](LICENSE.md) for details.
