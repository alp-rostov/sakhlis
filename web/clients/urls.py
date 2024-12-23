from django.urls import path

from clients.views import *

urlpatterns = [
    # path('clients/', Clients.as_view(), name='clients'),
    # path('clients/update/<int:pk>', ClientsUpdate.as_view(), name='clients_update'),

    path('', OwnerDetailInformation.as_view(), name='profile'),
    path('apartments', ApartmentOwner.as_view(), name='apartments_owner'),
    path('apartment/<int:pk>', OwnerApartmentUpdate.as_view(), name='apartment_update'),
    path('apartment/create', OwnerApartmentCreate.as_view(), name='apartment_create'),

    path('list_order', OwnerOrderManagementSystem.as_view(), name='o_list_order'),
    path('invoice/<int:pk>', OwnerInvoice.as_view(), name='ownerinvoice'),

]