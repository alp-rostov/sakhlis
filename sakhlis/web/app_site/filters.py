from django_filters import FilterSet
from .models import City

class CityFilter(FilterSet):
    class Meta:
        model = City
        fields = {'name': ['startswith']}
