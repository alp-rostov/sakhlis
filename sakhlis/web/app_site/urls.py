from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', OrderCreate.as_view(), name='new-oder'),
    path('list_order', OrderManagementSystem.as_view(), name='list_order'),
    path('list_order/<int:pk>', OrderDatail.as_view(), name='datail_order'),
    path('list_order/delete/<int:pk>', OrderDelete.as_view()),
    path('list_order/update/<int:pk>', OrderUpdate.as_view()),
    path('add', OrderAddRepaier),

    path('invoice/<int:order_pk>', InvoiceCreate.as_view()),

    path('list_repair', RepairerL.as_view(), name='list_repair'),
    path('list_repair/<int:pk>', RepaierD.as_view(), name='datail_repair'),
    path('create', RepaierCreate.as_view()),
    path('create/<int:pk>', RepaierUpdate.as_view()),
    path('delete/<int:pk>', RepaierDelete.as_view()),


    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', BaseRegisterView.as_view(template_name='register.html'), name='signup'),

    path('stat/', Statistica.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # для выгрузки картинок из БД в шаблон.
