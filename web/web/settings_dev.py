import os
from django.utils.encoding import force_str

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


CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

EMAIL_HOST = 'mail.sakhlis-remonti.ge'  # адрес сервера почты для всех один и тот же
EMAIL_PORT = 587  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'admin@sakhlis-remonti.ge'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = force_str(os.environ.get('EMAIL_PASSW'))   # пароль от почты
EMAIL_USE_SSL = False  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно





# Celery Configuration Options
CELERY_TIMEZONE = "Australia/Tasmania"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60




