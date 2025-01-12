# setup_django.py
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_db.settings")  # Replace with your Django project name
django.setup()


