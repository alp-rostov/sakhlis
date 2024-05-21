from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', OrderCreate.as_view(), name='home'),
    path('list_order', OrderManagementSystem.as_view(), name='list_order'),
    path('list_order/<int:pk>', InvoiceCreate.as_view(), name='invoice'),
    path('list_order/update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('list_order/pdf/<int:order_pk>', CreateIvoicePDF, name='invoice_pdf'),


    # path('new1', OrderCreatebyRepaier.as_view(), name='aaa'),





    path('update-user/<int:pk>', RepaierUpdate.as_view(), name='update-user'),

    path('add', OrderAddRepaier, name='add_repairer'),
    path('invoice/delete-order/<int:pk>', OrderDelete.as_view(), name='delete-order'),
    path('invoice/delete/<int:invoice_pk>', DeleteIvoiceService, name='delete-item-of-order'),

    path('login/', UserAuthorizationView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),

    path('register/', UserRegisterView.as_view(), name='signup'),
    path('error404/', Error404.as_view(), name='error404'),

    path('clients/', Clients.as_view(), name='clients'),

    path('stat/', Statistica.as_view(), name='stat'),
    path('user/<int:pk>', RepairerDetailInformation.as_view(), name='user'),



    path('owner/<int:pk>', OwnerDetailInformation.as_view(), name='owner'),
    path('owner-invoice/<int:pk>', OwnerInvoice.as_view(), name='ownerinvoice'),

    # path('app', AddApartment, name=''),

    path('ordersearch/', OrderSearchForm.as_view(), name='search-order'),

    path('serv', listservices_for_invoice_json),
    path('save_list', save_list_jobs),
    path('changestatus', change_work_status),
    path('client', client_details_json),
    # path('listorderjson', listorder_for_order_list_paginator_json),
    path('set_work_status', change_work_status),
    path('street', input_street),
    # path('geo', geo_map),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # для выгрузки картинок из БД в шаблон.
