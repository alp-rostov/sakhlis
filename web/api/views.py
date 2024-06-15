from django.db.models import Q
from rest_framework import serializers, generics

from app_site.models import UserProfile, StreetTbilisi, Apartment


class StreetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetTbilisi
        fields = ['type_street', 'name_street']

class ClientsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk', 'customer_name', 'phone', 'telegram']

class AppartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ['pk', 'address_street_app', 'address_num']


class StreetView(generics.ListAPIView):
    serializer_class = StreetModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        queryset = StreetTbilisi.objects.filter(name_street__istartswith=self.request.GET.get('street'))[0:15]
        return queryset

class StreetView(generics.ListAPIView):
    serializer_class = StreetModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        queryset = StreetTbilisi.objects.filter(name_street__istartswith=self.request.GET.get('street'))[0:15]
        return queryset

class ClientsView(generics.ListAPIView):
    serializer_class = ClientsModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        queryset = UserProfile.objects.filter(Q(customer_name__icontains=self.request.GET.get('client'))
                                              |Q(phone__icontains=self.request.GET.get('client'))
                                              |Q(telegram__icontains=self.request.GET.get('client')))[0:10]
        return queryset

class AppartView(generics.ListAPIView):
    serializer_class = AppartModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        queryset = Apartment.objects.filter(owner=self.request.GET.get('owner'))
        return queryset


