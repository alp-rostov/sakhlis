import os
import celery
from celery import Celery

print celery.__file__

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('website')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

