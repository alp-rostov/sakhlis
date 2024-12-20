from django.db import models
from django.contrib.auth.models import User

from app_site.constants import CITY_CHOICES
# from app_site.models import OrderList


class UserProfile(models.Model):
    """phone city foto rating_sum rating_num user"""
    customer_name = models.CharField(max_length=50, verbose_name='Name', null=True, blank=True)
    phone = models.CharField(max_length=16, verbose_name='Phone', null=True, blank=True)
    telegram = models.CharField(max_length=25, verbose_name='Telegram', null=True, blank=True)
    whatsapp = models.CharField(max_length=16, verbose_name='Whatsapp', null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB')
    profile = models.CharField(max_length=1500, null=True, blank=True, verbose_name='About me:')
    foto = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Photo:')
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'

    def __str__(self):
        return f"{self.customer_name}"


class ClientFeedback(models.Model):
    text_feedback = models.CharField(max_length=1500, verbose_name='Feedback', blank=True, null=True)
    mark = models.IntegerField(default=0, blank=True, null=True, verbose_name='Raiting')
    order_id = models.ForeignKey('app_site.OrderList', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Order')

    def __str__(self):
        return f'From: {self.order_id.customer_id.customer_name}, Messege: {self.text_feedback}'
