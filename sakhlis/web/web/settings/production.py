from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sakhlis',
        'USER': 'postgres',
        'PASSWORD': '1rostov1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log.log'),
            'formatter': 'simple'
        },
    },

    'style': '{',
    'formatters': {
        'simple': {
            'format':  '%(asctime)s   %(levelname)s  %(message)s  %(exc_info)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },

    },

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },

    }
}
