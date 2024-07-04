from django.urls import path

from api.views import *


urlpatterns = [
    path('street/', StreetView.as_view(), name='street'),
    path('getclient/', ClientsView.as_view(), name='getclient'),
    path('appart/', AppartView.as_view(), name='getappart'),
]