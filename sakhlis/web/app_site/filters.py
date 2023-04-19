from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import RepairerList, CityDirectory
from django import forms


class RepFilter(FilterSet):

    s_name = CharFilter(
        field_name='s_name',
        label='Фамилия',
        lookup_expr='startswith',
        widget=forms.TextInput(attrs={"class": "myfield"})
        )
    name = CharFilter(
            field_name='head_article',
            label='Имя',
            lookup_expr='startswith'
        )

    city_id = ModelChoiceFilter(
        field_name='city_id__name',
        label='Город',
        lookup_expr='exact',
        queryset=CityDirectory.objects.order_by('name').all(),
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
        fields = ['s_name', 'name', 'city_id', 'email', 'phone', ]
