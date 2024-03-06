import os

from .settings import *

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'sakhlis',
#         'USER': 'postgres',
#         'PASSWORD': '1rostov1',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }