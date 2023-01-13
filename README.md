# Django REST Framework Cookie Cutter
This is a simple Django REST Framework starter project. I've included:
- JWT Authentication
- Swagger/Redoc documentation
- Containerization
- Basic user management with a custom user model

## Getting started
To get up and running, just clone the repo and use docker to start it up:
```
git clone git@github.com:jayps/django-rest-framework-cookie-cutter.git
docker compose up -d
```

## Documentation
Once you're up and running, check out the documentation at [http://localhost:8000/swagger/](http://localhost:8000/swagger/).

## JWT Authentication
Check out the `/api/auth/register` and `/api/auth/login` endpoints to see how registration works.  
This API is made with a custom user model which uses the `email` field as the username.

## Adding your own code
To make sure that the correct version of Python and such is being used, keep things in docker.
Bash into the container: 
```
docker exec -it cookie-cutter-api bash
```

Run `django-admin` to create a new app:
```
cd cookiecutter # Replace cookiecutter with the name of your main folder if you renamed the cookiecutter folder.
django-admin startapp recipes # replace "recipes" with whatever your new app should be named.
```