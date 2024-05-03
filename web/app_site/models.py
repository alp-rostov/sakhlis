from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse

from .constants import CITY_CHOICES, ORDER_STATUS, WORK_CHOICES, QUANTITY_CHOICES

phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                                  message="Phone number must be entered in the "
                                          "format: '+999999999'. Up to 15 digits allowed.")

class Service(models.Model):
    """name type """
    name = models.\
        CharField(null=True, blank=True, max_length=500, verbose_name='Service') # better use default=""
    type = models.CharField(choices=WORK_CHOICES, null=True, blank=True, max_length=3, verbose_name='type of work')

    class Meta:
        ordering = ['type', 'name']
        verbose_name = 'Type of works'
        verbose_name_plural = 'Type of work'
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
    """time_in time_out repairer_id price text_order customer_name customer_phone address_city address_street_app
    address_num work_type services order_status"""
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Date of order')
    time_out = models.DateTimeField(null=True, blank=True, verbose_name='Order completion date')
    repairer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Мастер', default='', )
    apartment_id = models.ForeignKey('Apartment', on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Appartment', default='', )

    text_order = models.CharField(max_length=1500, verbose_name='Description of the problem', blank=True, null=True)


    customer_name = models.CharField(max_length=50, verbose_name='Name')
    customer_phone = models.CharField(max_length=16, verbose_name='Phone')
    customer_telegram = models.CharField(max_length=26, verbose_name='Telegram', blank=True, null=True)



    order_status = models.CharField(max_length=3, choices=ORDER_STATUS, default='BEG', null=True, blank=True,
                                    verbose_name='Order status')
    services = models.ManyToManyField('Service', through='Invoice')

    customer_code = models.CharField(max_length=16, verbose_name='Company code ', blank=True, null=True)
    address_city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB', null=True, blank=True,
                                    verbose_name='City')
    address_street_app = models.CharField(max_length=150, verbose_name='Street', null=True, blank=True)
    address_num = models.CharField(max_length=10, verbose_name='House number', null=True, blank=True)
    location_longitude = models.FloatField(verbose_name='Longitude', null=True, blank=True)
    location_latitude = models.FloatField(verbose_name='Latitude', null=True, blank=True)

    class Meta:
        verbose_name = 'Order list'
        verbose_name_plural = 'Order list'




class Repairer(models.Model):
    """phone city foto rating_sum rating_num user"""
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, verbose_name='Phone',
                             null=True, blank=True,)
    telegram = models.CharField(max_length=25, unique=True, verbose_name='Telegram',
                             null=True, blank=True, )
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB')
    profile = models.CharField(max_length=1500, null=True, blank=True, verbose_name='About me:')

    foto = models.ImageField(upload_to="images/repairer/", null=True, blank=True, verbose_name='Photo:')
    rating_sum = models.IntegerField(default=0, blank=True, null=True)
    rating_num = models.IntegerField(default=1, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'
    def get_absolute_url(self):
        return reverse('list_repair')


class Owner(models.Model):
    """"""
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, verbose_name='Phone',
                             null=True, blank=True, )
    telegram = models.CharField(max_length=25, unique=True, verbose_name='Telegram',
                                null=True, blank=True, )
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB')
    foto = models.ImageField(upload_to="images/owner", null=True, blank=True, verbose_name='Photo:')
    rating_sum = models.IntegerField(default=0, blank=True, null=True)
    rating_num = models.IntegerField(default=1, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Owner'
        verbose_name_plural = 'Owner'


class Apartment(models.Model):
    """"""
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Responsible person for apartment', default='', )

    address_city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB', null=True, blank=True,
                                    verbose_name='City')
    address_street_app = models.CharField(max_length=150, verbose_name='Street', null=True, blank=True)
    address_num = models.CharField(max_length=10, verbose_name='House number', null=True, blank=True)
    foto = models.ImageField(upload_to="images/appartment/", null=True, blank=True, verbose_name='Photo:')

    location_longitude = models.FloatField(verbose_name='Longitude', null=True, blank=True)
    location_latitude = models.FloatField(verbose_name='Latitude', null=True, blank=True)
    notes = models.CharField(max_length=1500, null=True, blank=True, verbose_name='Note:')

    class Meta:
        verbose_name = 'Appartment list'
        verbose_name_plural = 'Appartment list'




class StreerTbilisi(models.Model):
    type_street = models.CharField(max_length=50)
    name_street = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Street'
        verbose_name_plural = 'Street'

    def __str__(self):
        return f'{self.name_street} {self.type_street}'
