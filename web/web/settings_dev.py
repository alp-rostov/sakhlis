import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
 }

STATIC_URL = '/static/'
STATIC_DIR=os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]




