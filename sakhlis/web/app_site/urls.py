from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', OrderCreate.as_view(), name='home'),
    path('list_order', OrderManagementSystem.as_view(), name='list_order'),
    path('list_order/<int:pk>', OrderDatail.as_view(), name='list_detail'),


    path('list_order/update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('add', OrderAddRepaier, name='add_repairer'),

    path('invoice/<int:pk>', InvoiceCreate.as_view(), name='invoice'),

    path('invoice/delete-order/<int:pk>', OrderDelete.as_view(), name='delete-order'),
    path('invoice/delete/<int:invoice_pk>', DeleteIvoiceService, name='delete-item-of-order'),
    path('invoice/pdf/<int:order_pk>', CreateIvoicePDF, name='invoice_pdf'),





    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('register/', UserRegisterView.as_view(), name='signup'),


    path('stat/', Statistica.as_view(), name='stat'),
    path('repaierman/<int:pk>', RepaiermanSpace.as_view(), name='repaierman'),
    path('serv', listservices),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # для выгрузки картинок из БД в шаблон.
