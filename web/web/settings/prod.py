import os

from web.settings.base import BASE_DIR

ALLOWED_HOSTS = ['91.239.206.142', '127.0.0.1']


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

STATIC_ROOT=os.path.join(BASE_DIR,'staticprod/')

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
 }

DEBUG = False


CELERY_BROKER_URL = ''
CELERY_RESULT_BACKEND = ''
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

EMAIL_HOST = ''  # адрес сервера почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = ''  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = ''  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно


