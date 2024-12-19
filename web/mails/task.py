from celery import shared_task
from mails.models import Client
from time import sleep


@shared_task
def send_beat_offers():
    b=Client.objects.all().values_list('mail')
    for i in b:
        # send_email(email='alprostov.1982@gmail.com')
        print(i)
        sleep(1)
