
from rest_framework import serializers, generics

from app_site.models import OrderList, StreerTbilisi


class StreetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreerTbilisi
        fields = ['type_street', 'name_street']

class StreetView(generics.ListAPIView):
    serializer_class = StreetModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        queryset = StreerTbilisi.objects.filter(name_street__istartswith=self.request.GET.get('street'))[0:15]
        return queryset


