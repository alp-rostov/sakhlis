from django.db import models
from django.core.validators import RegexValidator

phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                                  message="Phone number must be entered in the "
                                          "format: '+999999999'. Up to 15 digits allowed.")

class City(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    repairer_id = models.ForeignKey("Repairer", on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(null=True)
    text_order = models.CharField(max_length=1500)
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(validators=[phoneNumberRegex], max_length=16)
    customer_feedback = models.CharField(max_length=1500, null=True)
    address_city_id = models.ForeignKey("City", on_delete=models.PROTECT)
    address_street_app = models.CharField(max_length=150)


class Repairer(models.Model):
    name = models.CharField(max_length=100)
    s_name = models.CharField(max_length=100, null=True)

    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)

    city_id = models.ForeignKey("City", on_delete=models.PROTECT)
    email = models.EmailField(max_length=200, null=True)
    foto = models.ImageField(upload_to="static/images", height_field=200,
                             width_field=200, null=True)
    active = models.BooleanField(default=False)
    rating_sum = models.IntegerField(default=0)
    rating_num = models.IntegerField(default=0)
