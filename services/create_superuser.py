from django.contrib.auth.models import User
import os

def create_superuser():
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

    if username and email and password:
        if not User.objects.filter(username=username).exists():
            print("Creating superuser...")
            User.objects.create_superuser(username, email, password)
        else:
            print("Superuser already exists")