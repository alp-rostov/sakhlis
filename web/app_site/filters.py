
from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter, MultipleChoiceFilter, \
    TypedMultipleChoiceFilter
from .models import *
from django import forms
#
class OrderFilter(FilterSet):


    time_in_sence = DateFilter(
        field_name="time_in__date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='From',
        lookup_expr='gte'
    )


    time_in_until = DateFilter(
        field_name="time_in__date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='To',
        lookup_expr='lte'
    )


    repairer_id = CharFilter(
        widget=forms.TextInput(attrs={"class": "hidden"}),
        label='Master-',
        lookup_expr='exact',

    )

    adress_street_app = CharFilter(
        field_name='address_street_app',
        label='Street',
        lookup_expr='icontains',

    )

    address_num = CharFilter(
        field_name='address_num',
        label='House number',
        lookup_expr='icontains',

    )

    customer_name = CharFilter(
        field_name='customer_name',
        label='Сustomer name',
        lookup_expr='icontains',

    )

    customer_phone = CharFilter(
        field_name='customer_phone',
        label='Phone',
        lookup_expr='icontains',

    )

    customer_telegram = CharFilter(
        field_name='customer_telegram',
        label='Telegram',
        lookup_expr='icontains',

    )

    address_city = ChoiceFilter(
        field_name='address_city',
        label='City',
        lookup_expr='icontains',
        choices=CITY_CHOICES,

    )

    address_city = ChoiceFilter(
        field_name='address_city',
        label='City',
        lookup_expr='icontains',
        choices=CITY_CHOICES,

    )

    class Meta:
        model = OrderList
        fields = ['order_status', 'repairer_id', 'address_city']


