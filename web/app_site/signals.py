import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import force_str

from .models import OrderList
from .tasks import send_order_information

@receiver(post_save, sender=OrderList)
def send_post_new_order(sender, instance, created, *args, **kwargs):
    """" """
    if created:
        # TOKEN_ = force_str(os.environ.get("TOKEN"))
        # CHAT_ID_ = force_str(os.environ.get("CHAT_ID"))
        TOKEN_= '6082335579:AAHqLPJB2RSdczDSbshpYV5Q7oqmyIcnbFI'
        CHAT_ID_= '5621399532'
        send_order_information.apply_async([instance.pk,TOKEN_, CHAT_ID_ ], countdown=5, expires=20)
        #send_order_information(instance.pk)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     """"create empty row in Repaierlist and sent a letter about registration."""
#     if created:
#         UserProfile.objects.create(user=instance)
        # my_group = Group.objects.get(name='repairer')
        # my_group.user_set.add(instance)
        # # send_email_after_registration.apply_async([instance.pk], countdown=5, expires=20)
