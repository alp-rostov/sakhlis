from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', OrderCreate.as_view(), name='home'),
    path('list_order', OrderManagementSystem.as_view(), name='list_order'),
    path('list_order/<int:pk>', OrderDatail.as_view(), name='list_detail'),
    path('list_order/delete/<int:pk>', OrderDelete.as_view(), name='delete'),
    path('list_order/update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('add', OrderAddRepaier, name='add_repairer'),

    path('invoice/<int:order_pk>', InvoiceCreate.as_view(), name='invoice'),
    path('invoice/delete/<int:invoice_pk>/<int:order_pk>', DeleteIvoiceService, name='delete_service_from_invoice'),
    path('invoice/pdf/<int:order_pk>', CreateIvoicePDF, name='invoice_pdf'),
    path('invoice/pdf_/<int:order_pk>', CreateIvoicePDF, ),

    path('list_repair', RepairerL.as_view(), name='list_repair'),
    path('list_repair/<int:pk>', RepaierD.as_view()),
    path('create', RepaierCreate.as_view()),
    path('create/<int:pk>', RepaierUpdate.as_view(), name='update_repair'),
    path('delete/<int:pk>', RepaierDelete.as_view(),  name='delete_repair'),


    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', BaseRegisterView.as_view(template_name='register.html'), name='signup'),

    path('stat/', Statistica.as_view(), name='stat'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # для выгрузки картинок из БД в шаблон.
