from weedstore.settings.base import *
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

STATIC_ROOT = '/home/ubuntu/static'
MEDIA_ROOT = '/home/ubuntu/media'

with open('/home/ubuntu/secret.txt') as f:
    SECRET_KEY = f.read().strip()
