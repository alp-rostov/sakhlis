from django.shortcuts import render
from rest_framework import generics

from api.views import StreetModelSerializer

#
# class StreetListApi(generics.ListAPIView):
#     """API for ajax request """
#     serializer_class = StreetModelSerializer
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         queryset = StreetTbilisi.objects.filter(name_street__istartswith=self.request.GET.get('street'))[0:10]
#         return queryset
