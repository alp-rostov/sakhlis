
from rest_framework import serializers, generics

from app_site.models import OrderList, StreetTbilisi


class StreetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetTbilisi
        fields = ['type_street', 'name_street']

class StreetView(generics.ListAPIView):
    serializer_class = StreetModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        queryset = StreetTbilisi.objects.filter(name_street__istartswith=self.request.GET.get('street'))[0:15]
        return queryset


