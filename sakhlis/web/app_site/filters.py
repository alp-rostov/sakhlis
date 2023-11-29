
from django_filters import FilterSet, CharFilter, DateFilter
from .models import *
from django import forms
#
# class RepFilter(FilterSet):
#
#
#     city = ChoiceFilter(
#         field_name='city',
#         label='Город',
#         lookup_expr='exact',
#         choices=CITY_CHOICES
#
#     )
#
#     email = CharFilter(
#         field_name='email',
#         label='E-mail',
#         lookup_expr='icontains'
#     )
#
#     phone = CharFilter(
#         field_name='phone',
#         label='Телефон',
#         lookup_expr='icontains'
#     )
#
#     class Meta:
#         model = RepairerList
#         fields = ['city', 'email', 'phone', ]


class OrderFilter(FilterSet):


    time_in_sence = DateFilter(
        field_name="time_in__date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='От',
        lookup_expr='gte'
    )


    time_in_until = DateFilter(
        field_name="time_in__date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='До',
        lookup_expr='lte'
    )




    repairer_id = CharFilter(
        widget=forms.TextInput(attrs={"class": "hidden"}),
        label='Мастер-',
        lookup_expr='exact',

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
        fields = ['order_status', 'repairer_id']


