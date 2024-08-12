# production.py

from .base import *

DEBUG = False

# The directory where static files will be collected
STATIC_ROOT = '/var/www/cyber.mrchen.store/static'

ALLOWED_HOSTS = ['localhost', 'cyber.mrchen.store']
