
from rest_framework import serializers, generics

from api.serialaizers import StreetModelSerializer
from app_site.models import OrderList, StreerTbilisi




class ApiStreetView(generics.ListAPIView):
    serializer_class = StreetModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        queryset = StreerTbilisi.objects.filter(name_street__istartswith=self.request.GET.get('street'))[0:15]
        return queryset

class ApiOrderListCreate(generics.ListAPIView):
    serializer_class = StreetModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        queryset = StreerTbilisi.objects.filter(name_street__istartswith=self.request.GET.get('street'))[0:15]
        return queryset



