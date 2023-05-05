from django_filters import FilterSet, ChoiceFilter, CharFilter, DateFilter
from .models import RepairerList, OrderList, AREA_CHOICES
from django import forms
from .models import CITY_CHOICES


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

    address_area = ChoiceFilter(
        field_name='address_area',
        label='Район',
        lookup_expr='exact',
        choices=AREA_CHOICES

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
        lookup_expr='exact',
    )

    time_out = DateFilter(
        field_name="time_out",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата выполнения заказа',
        lookup_expr='exact',
    )
    class Meta:
        model = OrderList
        fields = ['text_order', 'customer_name', 'customer_phone',
                  'address_city', 'address_area', 'address_street_app',
                  'time_in', 'time_out']

