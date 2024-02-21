from rest_framework import serializers

from app_site.models import StreerTbilisi


class StreetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreerTbilisi
        fields = ['type_street', 'name_street']