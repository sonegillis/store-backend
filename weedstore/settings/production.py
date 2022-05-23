from .base import *
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = '/home/ubuntu/static'
MEDIA_ROOT = '/home/ubuntu/media'

SECRET_KEY = env('SECRET_KEY')
HOST_DOMAIN = env('PRODUCTION_DOMAIN')

SMUGGLER_FIXTURE_DIR = '/home/ubuntu'
SMUGGLER_EXCLUDE_LIST = ['landing.cart', 'landing.cartItem']

CORS_ALLOWED_ORIGINS = [
    HOST_DOMAIN,
]
