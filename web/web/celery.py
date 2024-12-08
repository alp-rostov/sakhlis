import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'send-offers-every-5-minutes': {
        'task': 'app_site.tasks.send_beat_offers',
        'schedule': crontab(minute='*/1'),
    }
}