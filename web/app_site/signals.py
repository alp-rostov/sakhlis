from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from kombu.exceptions import OperationalError

from .models import OrderList, UserProfile
from .tasks import send_order_information,  task_save_location_
from .utils import Location

from django.contrib.auth.models import Group

@receiver(post_save, sender=OrderList)
def send_post_new_order(instance, created, **kwargs):
    """" """
    if created:
        task_save_location_.apply_async([instance.pk], countdown=5, expires=20)
        # send_order_information.apply_async([instance.pk], countdown=5, expires=20)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     """"create empty row in Repaierlist and sent a letter about registration."""
#     if created:
#         UserProfile.objects.create(user=instance)
        # my_group = Group.objects.get(name='repairer')
        # my_group.user_set.add(instance)
        # # send_email_after_registration.apply_async([instance.pk], countdown=5, expires=20)

