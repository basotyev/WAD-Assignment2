#!/usr/bin/env python
import os
import sys
import django
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


def create_superuser():
    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = 'adminpassword'

    try:
        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser {username}")
            User.objects.create_superuser(username=username, email=email, password=password)
        else:
            print(f"Superuser {username} already exists")
    except IntegrityError:
        print("Superuser creation failed. It may already exist.")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment2.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    if 'runserver' in sys.argv or 'migrate' in sys.argv:
        django.setup()
        create_superuser()


if __name__ == '__main__':
    main()
