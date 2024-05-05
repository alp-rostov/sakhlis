
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

    order_status = ChoiceFilter(
        field_name='order_status',
        label='Order_status',
        lookup_expr='icontains',
        choices=ORDER_STATUS,
    )

    class Meta:
        model = OrderList
        fields = ['order_status']



class ClientFilter(FilterSet):


    customer_name = CharFilter(
        field_name='customer_name',
        widget=forms.TextInput(attrs={"class": ""}),
        label='Name',
        lookup_expr='icontains',

    )

    phone = CharFilter(
        field_name='phone',
        label='Phone',
        lookup_expr='icontains',

    )

    telegram = CharFilter(
        field_name='telegram',
        label='Telegram',
        lookup_expr='icontains',

    )

    profile = CharFilter(
        field_name='profile',
        label='profile',
        lookup_expr='icontains',

    )

    #
    # address_city = ChoiceFilter(
    #     field_name='address_city',
    #     label='City',
    #     lookup_expr='icontains',
    #     choices=CITY_CHOICES,
    #
    # )
    #
    # address_city = ChoiceFilter(
    #     field_name='address_city',
    #     label='City',
    #     lookup_expr='icontains',
    #     choices=CITY_CHOICES,
    #
    # )

    class Meta:
        model = OrderList
        fields = ['customer_name', 'phone', 'telegram', 'profile']




