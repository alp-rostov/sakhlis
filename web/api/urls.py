from django.urls import path

from api.views import *

# noinspection PyPep8
urlpatterns = [
    path('street/', StreetView.as_view(), name='street'),
    path('orders/', OrderView.as_view()),

]