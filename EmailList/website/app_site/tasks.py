from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Email
from .utils import sentmail


@shared_task
def sent_to_users(news):
    queryset_mail = Email.objects.all()
    for i in queryset_mail:
        sentmail(i, news)

def sent_to_users1():
    print "dddddddddddd"
