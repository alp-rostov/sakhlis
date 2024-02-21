from celery import shared_task


from .models import Email
from .utils import sentmail


@shared_task
def sent_to_users(news,  idlist):
    queryset_mail = Email.objects.filter(pk__in=idlist)
    for i in queryset_mail:
        sentmail(i, news)

