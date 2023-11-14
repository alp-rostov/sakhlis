from django.contrib.auth.models import User
from django_filters import FilterSet, ChoiceFilter, CharFilter, DateFilter, BooleanFilter, ModelChoiceFilter
from .models import RepairerList, OrderList, StreerTbilisi
from .models import CITY_CHOICES
from django import forms

class RepFilter(FilterSet):


    city = ChoiceFilter(
        field_name='city',
        label='Город',
        lookup_expr='exact',
        choices=CITY_CHOICES

    )

    email = CharFilter(
        field_name='email',
        label='E-mail',
        lookup_expr='icontains'
    )

    phone = CharFilter(
        field_name='phone',
        label='Телефон',
        lookup_expr='icontains'
    )

    class Meta:
        model = RepairerList
        fields = ['city', 'email', 'phone', ]


class OrderFilter(FilterSet):


    time_in = DateFilter(
        field_name="time_in",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата поступления заказа',
        lookup_expr='icontains',
    )


    repairer_id = ModelChoiceFilter(
        field_name='repairer_id',
        label='Мастер-',
        lookup_expr='exact',
        queryset=User.objects.only('last_name', 'first_name'),
        null_label='Мастер не указан',
        empty_label='Все'

    )

    adress_street_app = CharFilter(
        field_name='address_street_app',
        label='Улица',
        lookup_expr='icontains',

    )

    address_num = CharFilter(
        field_name='address_num',
        label='Номер дома',
        lookup_expr='icontains',

    )

    customer_name = CharFilter(
        field_name='customer_name',
        label='Имя заказчика',
        lookup_expr='icontains',

    )

    customer_phone = CharFilter(
        field_name='customer_phone',
        label='Телефон',
        lookup_expr='icontains',

    )

    customer_telegram = CharFilter(
        field_name='customer_telegram',
        label='Телеграм',
        lookup_expr='icontains',

    )


    class Meta:
        model = OrderList
        fields = ['time_in', 'order_status', 'repairer_id']


