from rest_framework import serializers
from app_site.models import OrderList, Invoice
from django.contrib.auth.models import User

#
# class StreetModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StreetTbilisi
#         fields = ['type_street', 'name_street']


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderList
        fields = ['order_status']


class UpdateMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderList
        fields = ['repairer_id']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username',]
