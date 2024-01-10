from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from kombu.exceptions import OperationalError

from .models import OrderList, Repairer
from .tasks import send_order_information, send_email_after_registration
from .utils import set_coordinates_address


@receiver(post_save, sender=OrderList)
def send_post_new_order(instance, created, **kwargs):
    """"sent order`s information to telegram group"""
    try:
        if created:
            location = set_coordinates_address(instance.address_street_app, 'Тбилиси', instance.address_num)
            if location != None:
                instance.location_longitude=float(location[0])
                instance.location_latitude=float(location[1])
                instance.save()
            send_order_information.apply_async([instance.pk, location], countdown=5, expires=20)
    except OperationalError:
        print("ошибка отправки ассинхрон")  #TODO сделать запись в лог файл о несрабатывании ассинхрона

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """"create empty row in Repaierlist and sent a letter about registration."""
    if created:
        Repairer.objects.create(user=instance)
        # send_email_after_registration.apply_async([instance.pk], countdown=5, expires=20)

