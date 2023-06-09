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

    address_city = ChoiceFilter(
        field_name='address_city',
        label='Город',
        lookup_expr='exact',
        choices=CITY_CHOICES

    )

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
        queryset=RepairerList.objects.only('name', 's_name')
    )

    class Meta:
        model = OrderList
        fields = ['address_city', 'time_in', 'time_out', 'order_status', 'repairer_id']

