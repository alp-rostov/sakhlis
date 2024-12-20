import logging
import os

from django.utils.encoding import force_str
# from flask import request

try:
    from .settings_dev import *
except ImportError:
    from .settings_prod import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY=force_str(os.environ.get('SECRET_KEY'))

CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

logger = logging.getLogger('django')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style' : '{',
    'formatters': {
        'verbose_info': {
            'format': '%(asctime)s    %(levelname)s    %(module)s    %(message)s   %(pathname)s   %(exc_info)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },

    'handlers': {
        'security': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose_info'
        },
    },

    'loggers': {
        'django': {
            'handlers': ['security'],
            'propagate': True,
        },

    },
}

SECRET_KEY = force_str(os.environ.get('SECRET_KEY'))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'django.contrib.flatpages',
    'django_filters',
    'formtools',
    'slippers',
    'rest_framework',
    'django_cleanup.apps.CleanupConfig',
    # 'api.apps.ApiConfig',
    'debug_toolbar',
    'corsheaders',  # app is for giving permission to use api from other sources
    #_______________my app_________________________________________________
    'app_site.apps.AppSiteConfig',
    'mails.apps.MailsConfig',
    'clients.apps.ClientsConfig'
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',  # for translate
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
     'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
}

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
# LOGIN_REDIRECT_URL = f'/user/51'
LOGOUT_REDIRECT_URL = '/'

INTERNAL_IPS = [
    "127.0.0.1",
]

DEFAULT_CHARSET = 'utf-8'

handler404 = 'app_site.views.Error404.as_view()'

