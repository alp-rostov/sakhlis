import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OrderList
from .tasks import send_to_telegrambot, send_email


@receiver(post_save, sender=OrderList)
def send_order_to_telegrambot(sender, instance, created, *args, **kwargs):
    """" """
    if created:
        # TOKEN_ = force_str(os.environ.get("TOKEN"))
        # CHAT_ID_ = force_str(os.environ.get("CHAT_ID"))
        TOKEN_= '6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI'
        CHAT_ID_= '5621399532'
        send_to_telegrambot.apply_async([instance.pk,TOKEN_, CHAT_ID_ ], countdown=5, expires=20)
        #send_order_information(instance.pk)

@receiver(post_save, sender=User)
def send_email_after_registration(sender, instance, created, **kwargs):
    if created:
        send_email.apply_async([instance.pk, instance.username, instance.email], countdown=5, expires=20)
