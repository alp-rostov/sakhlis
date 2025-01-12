from django.contrib.auth.models import User
from django.db import models

from apartments.models import Apartment
from .constants import ORDER_STATUS, WORK_CHOICES, QUANTITY_CHOICES


class Service(models.Model):
    """name type """
    name = models.\
        CharField(null=True, blank=True, max_length=500, verbose_name='Service')  # better use default=""
    type = models.CharField(choices=WORK_CHOICES, null=True, blank=True, max_length=3, verbose_name='type of work')

    class Meta:
        ordering = ['type', 'name']
        verbose_name = 'Type of work'
        verbose_name_plural = 'Type of works'

    def __str__(self):
        return f"{self.name}"


class Invoice(models.Model):
    """service_id order_id quantity_type quantity price"""
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE, null=True, blank=True, )
    order_id = models.ForeignKey('OrderList', on_delete=models.CASCADE, null=True, blank=True, )
    quantity_type = models.CharField(choices=QUANTITY_CHOICES, max_length=3, null=True, blank=True,
                                     verbose_name='Measurement')
    quantity = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True, verbose_name='Quantity')
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True, verbose_name='Price')

    class Meta:
        verbose_name = 'Work`s list of the order'
        verbose_name_plural = 'Work`s list of the order'

    def __str__(self):
        return f"{self.service_id}"


class OrderList(models.Model):
    """List of repair orders"""
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Date of order')
    time_out = models.DateTimeField(null=True, blank=True, verbose_name='Order completion date')

    repairer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Repairer', )
    apartment_id = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Appartment', )
    customer_id = models.ForeignKey('clients.UserProfile', on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Client', )

    text_order = models.CharField(max_length=1500, verbose_name='Description of the problem', blank=True, null=True)

    order_status = models.CharField(max_length=3, choices=ORDER_STATUS, default='SND', null=True, blank=True,
                                    verbose_name='Order status')
    services = models.ManyToManyField('Service', through='Invoice')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
