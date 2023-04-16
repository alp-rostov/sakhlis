from django_filters import FilterSet
from .models import City, Repairer

class CityFilter(FilterSet):
    class Meta:
        model = City
        fields = {'name': ['startswith']}

class RepFilter(FilterSet):
    class Meta:
        model = Repairer
        fields = {'name': ['startswith'],
                  's_name': ['startswith'],
                  'email': ['icontains'],
                  'phone': ['icontains'],
                  'rating_sum':['lt','gt']
                  }