from django.urls import path

from api.views import *


urlpatterns = [
    path('street/', StreetView.as_view(), name='street'),
    # path('apartments/', AppartList.as_view(), name='apartments'),

]