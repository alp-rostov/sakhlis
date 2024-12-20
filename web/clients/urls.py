from django.urls import path

from clients.views import *

urlpatterns = [
    path('clients/', Clients.as_view(), name='clients'),
    path('clients/update/<int:pk>', ClientsUpdate.as_view(), name='clients_update'),

]