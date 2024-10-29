from time import strptime

from django.db.models import F
from rest_framework import serializers, generics
from django.contrib.auth.models import User
from app_site.models import UserProfile, StreetTbilisi, Apartment, OrderList


class StreetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetTbilisi
        fields = ['type_street', 'name_street']



class CustomerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk', 'customer_name', 'user']

class ApartmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ['pk', 'address_city', 'name',
                          'address_street_app', 'address_num',]

class RepaierModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username']


class OrderModelSerializer(serializers.ModelSerializer):
    customer_id = CustomerModelSerializer(required=False)
    apartment_id = ApartmentModelSerializer(required=False)
    repairer_id = RepaierModelSerializer(required=False)
    class Meta:
        model = OrderList
        fields =['pk', 'time_in', 'repairer_id',
                            'text_order', 'apartment_id',
                            'customer_id']

class StreetView(generics.ListAPIView):
    serializer_class = StreetModelSerializer
    http_method_names = ['get']
    def get_queryset(self):
        return StreetTbilisi.objects.all()

class OrderView(generics.ListAPIView):
    serializer_class = OrderModelSerializer
    http_method_names = ['get']
    queryset = OrderList.objects.select_related('customer_id',
                                                'apartment_id',
                                                'repairer_id').all()[::-1]
    print(queryset[2])


