# production.py

from .base import *


DEBUG = False

import os
try:
    SECRET_KEY = os.environ["SECRET_KEY"]
except KeyError as e:
    raise RuntimeError("Could not find a SECRET_KEY in environment") from e

# The directory where static files will be collected
STATIC_ROOT = '/var/www/cyber.mrchen.store/static'

ALLOWED_HOSTS = ['localhost', 'cyber.mrchen.store']
