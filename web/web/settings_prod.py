import os
from django.utils.encoding import force_str
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

ALLOWED_HOSTS = ['91.239.206.142', 'www.sakhlis-remonti.ge', 'www.sakhlis-remonti.ge', 'sakhlis-remonti.ge', 'sakhlis-remonti.ge', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
 }

CSRF_TRUSTED_ORIGINS = ['http://sakhlis-remonti.ge', 'https://sakhlis-remonti.ge','https://www.sakhlis-remonti.ge', 'http://www.sakhlis-remonti.ge']

STATIC_URL = '/static/'
STATIC_DIR=os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

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


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Celery Configuration Options
CELERY_TIMEZONE = "Australia/Tasmania"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60



EMAIL_HOST = 'mail.sakhlis-remonti.ge'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@sakhlis-remonti.ge'
EMAIL_HOST_PASSWORD = force_str(os.environ.get('EMAIL_PASSW'))
EMAIL_USE_SSL = False
