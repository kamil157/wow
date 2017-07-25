import os

from configurations import importer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wow.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
importer.install(check_options=True)
