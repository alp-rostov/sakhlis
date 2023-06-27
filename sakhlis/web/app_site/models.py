from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.urls import reverse

phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                                  message="Phone number must be entered in the "
                                          "format: '+999999999'. Up to 15 digits allowed.")
CITY_CHOICES = [
    ('TB', 'Тбилиси'),
    ('BT', 'Батуми'),
    ('RS', 'Рустави'),
]

WORK_CHOICES = [
    ('EL', 'Электрика'),
    ('PL', 'Сантехника'),
    ('SP', 'Кондиционирование'),
    ('FT', 'Ремонт/сборка мебели'),
    ('OT', 'Ремонт окон, дверей'),

]
QUANTITY_CHOICES = [
    ('SV', 'Услуга'),
    ('ME', 'Метр'),
    ('QL', 'Килограмм'),
    ('TH', 'Штука'),

]

QUANTITY_CHOICES = [
    ('SV', 'Услуга'),
    ('ME', 'Метр'),
    ('QL', 'Килограмм'),
    ('TH', 'Штука'),

]

ORDER_STATUS = [
    ('BEG', 'Заявка получен'),
    ('SND', 'Направлена мастеру'),
    ('END', 'Заявка выполнена'),
    ('CNL', 'Заявка отменена'),

]

MONTH = [
    (1, 'Январь'),
    (2, 'Февраль'),
    (3, 'Март'),
    (4, 'Апрель'),
    (5, 'Май'),
    (6, 'Июнь'),
    (7, 'Июль'),
    (8, 'Август'),
    (9, 'Сентябрь'),
    (10, 'Октябрь'),
    (11, 'Ноябрь'),
    (12, 'Декабрь'),

]

class Service(models.Model):
    """name type """
    name = models.\
        CharField(null=True, blank=True, max_length=500, verbose_name='Услуга')
    type = models.CharField(choices=WORK_CHOICES, null=True, blank=True, max_length=3, verbose_name='Вид работ')

    def __str__(self):
        return f"{self.name}"


class Invoice(models.Model):
    """service_id order_id quantity_type quantity price"""
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE, null=True, blank=True, )
    order_id = models.ForeignKey('OrderList', on_delete=models.CASCADE, null=True, blank=True, )
    quantity_type = models.CharField(choices=QUANTITY_CHOICES, max_length=3, null=True, blank=True,
                                     verbose_name='Измерение')
    quantity = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True, verbose_name='Количество')
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True, verbose_name='Цена')

    def __str__(self):
        return f"{self.quantity}"


class OrderList(models.Model):
    """time_in time_out repairer_id price text_order customer_name customer_phone address_city address_street_app
    address_num work_type services order_status"""
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    time_out = models.DateTimeField(null=True, blank=True, verbose_name='Дата выполнения')
    repairer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Мастер', default='', )
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True, verbose_name='Стоимость работ')
    text_order = models.CharField(max_length=1500, verbose_name='Описание проблемы', blank=True, null=True)
    customer_name = models.CharField(max_length=50, verbose_name='Ваше имя')
    customer_phone = models.CharField(max_length=16, verbose_name='Номер телефона')
    customer_code = models.CharField(max_length=16, verbose_name='Код организации', blank=True, null=True)
    address_city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB', null=True, blank=True,
                                    verbose_name='Город')
    order_status = models.CharField(max_length=3, choices=ORDER_STATUS, default='BEG', null=True, blank=True,
                                    verbose_name='Статус заказа')
    address_street_app = models.CharField(max_length=150, verbose_name='Улица', null=True, blank=True)
    address_num = models.CharField(max_length=10, verbose_name='Номер дома', null=True, blank=True)
    services = models.ManyToManyField('Service', through='Invoice')

    def __str__(self):
        return f"{self.customer_name}"


class RepairerList(models.Model):
    """name s_name phone city email foto active rating_sum rating_num"""
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, verbose_name='Телефон')
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='TB')
    foto = models.ImageField(upload_to="images/", null=True, blank=True, verbose_name='Фотография:')
    rating_sum = models.IntegerField(default=0, blank=True, null=True)
    rating_num = models.IntegerField(default=0, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)


    def get_absolute_url(self):
        return reverse('list_repair')
