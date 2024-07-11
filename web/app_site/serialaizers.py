from rest_framework import serializers, generics
from app_site.models import UserProfile, StreetTbilisi, Apartment, OrderList


class StreetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreetTbilisi
        fields = ['type_street', 'name_street']


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderList
        fields = ['order_status']
