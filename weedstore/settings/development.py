from .base import *
import os
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.dPASlinuxSWORDb.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': env('DB_NAME'),

        'USER': env('DB_USER'),

        'PASSWORD': env('DB_PASSWORD'),

        'HOST': 'localhost',

        'PORT': '5432',

    }
}

SMUGGLER_FIXTURE_DIR = ''
SMUGGLER_EXCLUDE_LIST = ['landing.cart', 'landing.cartItem']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# HOST_DOMAIN = "http://192.168.100.22:4200"
HOST_DOMAIN = "http://172.20.10.3:4200"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:8100",
    "http://192.168.100.21:4200",
    "http://192.168.100.22:4200",
    "http://192.168.100.22:8100",
    "http://192.168.100.23:4200",
    "http://172.20.10.3:4200"
]
