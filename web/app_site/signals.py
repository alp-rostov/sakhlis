import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderList, UserProfile
from .tasks import send_to_telegrambot, send_email


@receiver(post_save, sender=OrderList)
def send_order_to_telegrambot(sender, instance, created, *args, **kwargs):
    if created:
        send_to_telegrambot.apply_async([instance.pk], countdown=5, expires=20)

@receiver(post_save, sender=User)
def send_email_after_registration(sender, instance, created, **kwargs):
    if created:
        context={'pk':instance.pk,'username':instance.username}
        subject_='User registration | sakhlis-remonti.ge'
        send_email.apply_async([instance.email, subject_, 'emails/registration.html', context],
                               countdown=5, expires=20)
