from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import City, Repairer
from django import forms

class CityFilter(FilterSet):
    class Meta:
        model = City
        fields = {'name': ['startswith']}

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
        queryset=City.objects.order_by('name').all(),
        lookup_expr='exact'
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
        model = Repairer
        fields = ['s_name', 'name', 'city_id', 'email', 'phone', ]



