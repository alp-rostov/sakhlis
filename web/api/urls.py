from django.urls import include

from django.urls import path
from rest_framework.templatetags import rest_framework

from api.views import *

# noinspection PyPep8
urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('street/', StreetView.as_view(), name='street'),
    path('orders/', OrderView.as_view()),


]