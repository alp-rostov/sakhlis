from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderList
from .tasks import send_order_information

TOKEN = "6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI"
CHAT_ID = 5621399532


@receiver(post_save, sender=OrderList)
def send_post_new_order(instance, created, **kwargs):
    if created:
        send_order_information.apply_async([instance.pk], countdown=20, expires=3600)

