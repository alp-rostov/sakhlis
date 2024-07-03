from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', OrderCreate.as_view(), name='home'),
    path('list_order', OrderManagementSystem.as_view(), name='list_order'),
    path('list_order/<int:pk>', InvoiceCreate.as_view(), name='invoice'),
    path('list_order/update/<int:pk>', OrderUpdate.as_view(), name='update-order'),
    path('list_order/pdf/<int:order_pk>', CreateIvoicePDF, name='invoice_pdf'),

    path('update-user/<int:pk>', RepaierUpdate.as_view(), name='update-user'),

    path('add', OrderAddRepaier, name='add_repairer'),
    path('invoice/delete-order/<int:pk>', OrderDelete.as_view(), name='delete-order'),
    path('invoice/delete/<int:invoice_pk>', DeleteIvoiceService, name='delete-item-of-order'),

    path('login/', UserAuthorizationView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),

    path('register/', UserRegisterView.as_view(), name='signup'),
    path('error404/', Error404.as_view(), name='error404'),

    path('clients/', Clients.as_view(), name='clients'),
    path('clients/update/<int:pk>', ClientsUpdate.as_view(), name='clients_update'),
    path('apartments/', ApartmentList.as_view(), name='apartments'),
    path('apartments/update/<int:pk>', ApartmentUpdate.as_view(), name='apart'),

    path('stat/', Statistica.as_view(), name='stat'),
    path('user/<int:pk>', RepairerDetailInformation.as_view(), name='user'),



    path('owner/apartment', OwnerDetailInformation.as_view(), name='apartment'),
    path('owner/apartment/<int:pk>', OwnerApartmentUpdate.as_view(), name='apartment_update'),
    path('owner/apartment/create', OwnerApartmentCreate.as_view(), name='apartment_create'),
    path('owner/list_order', OwnerOrderManagementSystem.as_view(), name='o_list_order'),
    path('owner-invoice/<int:pk>', OwnerInvoice.as_view(), name='ownerinvoice'),


    # path('ordersearch/', OrderSearchForm.as_view(), name='search-order'),

    path('serv', listservices_for_invoice_json),
    path('save_list', save_list_jobs),
    path('changestatus', change_work_status),
    path('client', client_details_json),
    # path('listorderjson', listorder_for_order_list_paginator_json),
    path('set_work_status', change_work_status),
    path('street', input_street),
    # path('create_order_by_owner', creat_order_from_owner_profile),
    # path('geo', geo_map),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # для выгрузки картинок из БД в шаблон.
