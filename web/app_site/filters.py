
from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter, ModelChoiceFilter
from .models import *
from django import forms


class OrderFilter(FilterSet):
    time_in_sence = DateFilter(
        field_name="time_in__date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'mr-3', }),
        label='From',
        lookup_expr='gte'
    )
    time_in_until = DateFilter(
        field_name="time_in__date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'mr-3', }),
        label='To',
        lookup_expr='lte'
    )
    order_status = ChoiceFilter(
        field_name='order_status',
        label='Order_status',
        lookup_expr='icontains',
        choices=ORDER_STATUS,
        empty_label='Choose order status'

    )
    repairer_id = ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='repairer_id',
        label='Master',
        empty_label='Choose master'

    )

    class Meta:
        model = OrderList
        fields = ['order_status', 'repairer_id']


class ClientFilter(FilterSet):
    customer_name = CharFilter(
        field_name='customer_name',
        widget=forms.TextInput(attrs={"class": "", "placeholder": "Customer`s name"}),
        label='',
        lookup_expr='icontains',

    )
    phone = CharFilter(
        field_name='phone',
        widget=forms.TextInput(attrs={"class": "", "placeholder": "phone", "size": "12"}),
        label='',
        lookup_expr='icontains',
    )
    telegram = CharFilter(
        field_name='telegram',
        widget=forms.TextInput(attrs={"class": "", "placeholder": "telegram", "size": "12"}),
        label='',
        lookup_expr='icontains',
    )
    profile = CharFilter(
        field_name='profile',
        label='',
        widget=forms.TextInput(attrs={"class": "", "placeholder": "about customer"}),
        lookup_expr='icontains',
    )

    class Meta:
        model = OrderList
        fields = ['customer_name', 'phone', 'telegram', 'profile']


class ApartmentFilter(FilterSet):
    address_street_app = CharFilter(
        field_name='address_street_app',
        label='',
        widget=forms.TextInput(attrs={"class": "", "placeholder": "Street"}),
        lookup_expr='icontains',
    )
    address_city = ChoiceFilter(
        field_name='address_city',
        label='City',
        lookup_expr='icontains',
        choices=CITY_CHOICES,
    )

    class Meta:
        model = OrderList
        fields = ['address_city']
