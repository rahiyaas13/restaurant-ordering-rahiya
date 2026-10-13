"""Create a superuser from environment variables (idempotent).

Used by render.yaml so /admin/ and the kitchen dashboard work after deploy.
Set DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD (and optionally
DJANGO_SUPERUSER_EMAIL). An existing user is never modified.
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_project.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

if not password:
    print("DJANGO_SUPERUSER_PASSWORD not set - skipping superuser creation.")
elif User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists - nothing to do.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
