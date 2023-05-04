from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import OrderList, AREA_CHOICES
from geopy.geocoders import Nominatim
import telebot
from .tasks import send_order_information
TOKEN = "6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI"
CHAT_ID = 5621399532


@receiver(post_save, sender=OrderList)
def send_post_new_order(instance, created, **kwargs):
    if created:
        send_order_information.delay(instance.pk)

