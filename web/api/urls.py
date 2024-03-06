from django.urls import path

from api.views import StreetView


urlpatterns = [
    path('street/', StreetView.as_view(), name='street'),

]