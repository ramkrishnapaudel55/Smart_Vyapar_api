from pathlib import Path
from decouple import config, Csv
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = config('ALLOWED_HOSTS', default="localhost", cast=Csv())

CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default="localhost", cast=Csv())

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default="localhost", cast=Csv())

