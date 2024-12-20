from django.db import models
from django.contrib.auth.models import User

from app_site.constants import CITY_CHOICES


class MasterProfile(models.Model):
    """Masters` List """
    phone = models.CharField(max_length=16, verbose_name='Phone', null=True, blank=True)
    telegram = models.CharField(max_length=25, verbose_name='Telegram', null=True, blank=True)
    whatsapp = models.CharField(max_length=16, verbose_name='Whatsapp', null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB')
    profile = models.CharField(max_length=1500, null=True, blank=True, verbose_name='Profile:')
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
