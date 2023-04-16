from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                                  message="Phone number must be entered in the "
                                          "format: '+999999999'. Up to 15 digits allowed.")

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    repairer_id = models.ForeignKey("Repairer", on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(null=True, validators=[MinValueValidator(0.0)])
    text_order = models.CharField(max_length=1500, verbose_name='Описание проблемы')
    customer_name = models.CharField(max_length=50, verbose_name='Ваше имя')
    customer_phone = models.CharField(validators=[phoneNumberRegex], max_length=16, verbose_name='Номер телефона')
    customer_feedback = models.CharField(max_length=1500, null=True)
    address_city_id = models.ForeignKey("City", on_delete=models.PROTECT, verbose_name='Город')
    address_street_app = models.CharField(max_length=150, verbose_name='Адрес')


class Repairer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    s_name = models.CharField(max_length=100, null=True, verbose_name='Фамилия')

    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, verbose_name='Телефон')

    city_id = models.ForeignKey("City", on_delete=models.PROTECT, verbose_name='Город', related_name='city')
    email = models.EmailField(max_length=200, null=True, verbose_name='Электронная почта')
    foto = models.ImageField(upload_to="images/",  null=True, blank=True, verbose_name='Фотография:')
    active = models.BooleanField(default=False)
    rating_sum = models.IntegerField(default=0)
    rating_num = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} {self.s_name}"
