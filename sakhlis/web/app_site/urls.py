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

    path('add', OrderAddRepaier, name='add_repairer'),
    path('invoice/delete-order/<int:pk>', OrderDelete.as_view(), name='delete-order'),
    path('invoice/delete/<int:invoice_pk>', DeleteIvoiceService, name='delete-item-of-order'),

    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),

    path('register/', UserRegisterView.as_view(), name='signup'),
    path('error404/', Error404.as_view(), name='error404'),

    path('stat/', Statistica.as_view(), name='stat'),
    path('user/<int:pk>', UserDetailInformation.as_view(), name='user'),
    path('update-user/<int:pk>', RepaierUpdate.as_view(), name='update-user'),

    path('ordersearch/', OrderSearchForm.as_view(), name='search-order'),

    path('serv', listservices_for_invoice_json),
    path('changestatus', change_work_status),

    path('listorderjson', listorder_for_order_list_paginator_json),
    path('set_work_status', change_work_status),
    # path('street', input_street),
    # path('geo', geo_map),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # для выгрузки картинок из БД в шаблон.
