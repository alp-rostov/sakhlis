from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *


urlpatterns = [
    path('', OrderCreate.as_view(), name='home'),
    path('en', OrderCreate.as_view(template_name='order_create_en.html'), name='home_en'),
    path('ge', OrderCreate.as_view(template_name='order_create_ge.html'), name='home_ge'),
    path('corporate', TemplateView.as_view(template_name='business.html'), name='business'),
    path('corporate_en', TemplateView.as_view(template_name='business_en.html'), name='business_en'),
    path('corporate_ge', TemplateView.as_view(template_name='business_ge.html'), name='business_ge'),

    path('masters', TemplateView.as_view(template_name='masters.html'), name='masters'),

    path('createorder', OrderCreate.as_view(template_name='createorder.html'), name='createorder'),
    path('createorder_en', OrderCreate.as_view(template_name='createorder_en.html'), name='createorder_en'),
    path('createorder_ge', OrderCreate.as_view(template_name='createorder_ge.html'), name='createorder_ge'),

    path('list_order', OrderManagementSystem.as_view(), name='list_order'),
    # path('street', OrdersOnTheStreet.as_view(), name='aaa'),
    path('list_order/<int:pk>', InvoiceCreate.as_view(), name='invoice'),
    path('list_order/update/<int:pk>', OrderUpdate.as_view(), name='update-order'),

    path('list_order/pdf/<int:order_pk>', CreateIvoicePDF, name='invoice_pdf'),



    path('update-user/<int:pk>', RepaierUpdate.as_view(), name='update-user'),

    path('add', OrderAddRepaier, name='add_repairer'),
    path('invoice/delete-order/<int:pk>', OrderDelete.as_view(), name='delete-order'),
    # path('deleteservice/<int:invoice_pk>', DeleteIvoiceServiceAPI.as_view(), name='delete-item-of-order'),

    path('login/', UserAuthorizationView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),

    path('register/', UserRegisterView.as_view(), name='signup'),
    path('error404/', Error404.as_view(), name='error404'),
    path('registration/', InfoTemplate.as_view(extra_context = {'title':'Thank you for registration',
                                                            'info':'Please check your email and confirm your account'}),
                                           name='message_after_registration'),
    path('confirm_registration/', InfoTemplate.as_view(extra_context={'title': 'Your account has been verified',
                                                          'info': ''}),
         name='confirm_registration'),


    path('clients/', Clients.as_view(), name='clients'),
    path('clients/update/<int:pk>', ClientsUpdate.as_view(), name='clients_update'),
    path('apartments/', ApartmentList.as_view(), name='apartments'),
    path('apartments/update/<int:pk>', ApartmentUpdate.as_view(), name='apart'),

    path('stat/', Statistica.as_view(), name='stat'),
    path('user/<int:pk>', RepairerDetailInformation.as_view(), name='user'),

    path('owner/profile', OwnerDetailInformation.as_view(), name='profile'),
    path('owner/apartments', ApartmentOwner.as_view(), name='apartments_owner'),

    path('owner/apartment/<int:pk>', OwnerApartmentUpdate.as_view(), name='apartment_update'),
    path('owner/apartment/create', OwnerApartmentCreate.as_view(), name='apartment_create'),
    path('owner/list_order', OwnerOrderManagementSystem.as_view(), name='o_list_order'),
    path('owner-invoice/<int:pk>', OwnerInvoice.as_view(), name='ownerinvoice'),

    path('serv', listservices_for_invoice_json),


    path('sendoffer', SendOffer.as_view(), name='sendoffer'),

    path('save_list', save_list_jobs),
    path('client', client_details_json),
    # path('listorderjson', listorder_for_order_list_paginator_json),
    path('street', StreetListApi.as_view()),
    path('orderstatus/<int:pk>', OrderStatusUpdateAPI.as_view()),
    path('deleteinvoice/<int:pk>', DeleteIvoiceServiceAPI.as_view()),
    path('masters', MastersListAPI.as_view()),
    path('setmaster/<int:pk>', MasterUpdateAPI.as_view()),
    path('verification', verife_account),
]


