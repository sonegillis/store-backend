from .base import *
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = 'static/'
MEDIA_ROOT = '/home/ubuntu/media'

SECRET_KEY = env('SECRET_KEY')
HOST_DOMAIN = env('PRODUCTION_DOMAIN')

SMUGGLER_FIXTURE_DIR = '/'

CORS_ALLOWED_ORIGINS = [
    HOST_DOMAIN,
]
