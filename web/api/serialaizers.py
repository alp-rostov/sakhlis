from rest_framework import serializers, generics
from app_site.models import UserProfile, StreetTbilisi, Apartment


class ApartmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ['pk', 'address_city', 'address_street_app', 'address_num']
