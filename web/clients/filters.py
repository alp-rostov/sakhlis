from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter, ModelChoiceFilter
from .models import *
from django import forms


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


