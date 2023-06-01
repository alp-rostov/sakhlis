from pprint import pprint

from django_filters import FilterSet, ChoiceFilter, CharFilter, DateFilter, BooleanFilter, ModelChoiceFilter
from .models import RepairerList, OrderList
from .models import CITY_CHOICES
from django import forms

class RepFilter(FilterSet):

    s_name = CharFilter(
        field_name='s_name',
        label='Фамилия',
        lookup_expr='startswith',
        widget=forms.TextInput(attrs={"class": "myfield"})
        )
    name = CharFilter(
            field_name='name',
            label='Имя',
            lookup_expr='startswith'
        )

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
        fields = ['s_name', 'name', 'city', 'email', 'phone', ]


class OrderFilter(FilterSet):
    text_order = CharFilter(
        field_name='text_order',
        label='Описание проблемы',
        lookup_expr='startswith',
        widget=forms.TextInput(attrs={"class": "myfield"})
    )
    customer_name = CharFilter(
        field_name='customer_name',
        label='Имя клиента',
        lookup_expr='startswith'
    )

    customer_phone = CharFilter(
        field_name='customer_phone',
        label='Телефон',
        lookup_expr='icontains'
    )

    address_city = ChoiceFilter(
        field_name='address_city',
        label='Город',
        lookup_expr='exact',
        choices=CITY_CHOICES

    )

    address_street_app = CharFilter(
        field_name='street',
        label='Улица',
        lookup_expr='icontains'
    )

    time_in = DateFilter(
        field_name="time_in",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата поступления заказа',
        lookup_expr='icontains',
    )

    time_out = BooleanFilter(
        field_name='time_out',
        label='Текущие работы',
        lookup_expr='isnull',
        widget=forms.Select(attrs={'class': 'sss'},  choices=[('', 'Все'), ('True', 'в работе'), ('False', 'выполнено')]),
    )
    repairer_id = ModelChoiceFilter(
        field_name='repairer_id',
        label='Мастер-',
        lookup_expr='exact',
        queryset=RepairerList.objects.only('name', 's_name')
    )

    class Meta:
        model = OrderList
        fields = ['text_order', 'customer_name', 'customer_phone',
                  'address_city', 'address_street_app',
                  'time_in', 'time_out', 'repairer_id']

