from django.db import models
from django.core.validators import RegexValidator

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

class OrderCategory(models.Model):
    pass
class OrderList(models.Model):
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    time_out = models.DateTimeField(null=True, blank=True, verbose_name='Дата выполнения')
    repairer_id = models.ForeignKey("RepairerList", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Мастер', default='',)
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True,  verbose_name='Стоимость работ')
    text_order = models.CharField(max_length=1500, verbose_name='Описание проблемы', blank=True, null=True)
    customer_name = models.CharField(max_length=50, verbose_name='Ваше имя')
    customer_phone = models.CharField(max_length=16, verbose_name='Номер телефона')
    address_city = models.CharField(max_length=2, choices=CITY_CHOICES,  default='TB', null=True, blank=True, verbose_name='Город')
    work_type = models.CharField(max_length=3, choices=WORK_CHOICES, default='', null=True, blank=True, verbose_name='Вид работ')
    address_street_app = models.CharField(max_length=150, verbose_name='Улица', null=True, blank=True)
    address_num = models.CharField(max_length=10, verbose_name='Номер дома', null=True, blank=True)


class RepairerList(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    s_name = models.CharField(max_length=100, null=True, verbose_name='Фамилия')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, verbose_name='Телефон')
    city = models.CharField(max_length=2, choices=CITY_CHOICES,  default='TB')
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name='Электронная почта')
    foto = models.ImageField(upload_to="images/",  null=True, blank=True, verbose_name='Фотография:')
    active = models.BooleanField(default=False)
    rating_sum = models.IntegerField(default=0, blank=True, null=True)
    rating_num = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.s_name}"

    def get_absolute_url(self):
        return reverse('list_repair')
