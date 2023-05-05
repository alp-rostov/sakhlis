from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import RepairerL, RepaierD, RepaierCreate, RepaierUpdate, RepaierDelete, BaseRegisterView, NewOrder, \
    OrderManagementSystem, OrderDelete, OrderDatail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', NewOrder.as_view(), name='new-oder'),
    path('list_order', OrderManagementSystem.as_view(), name='list_order'),
    path('list_order/<int:pk>', OrderDatail.as_view(), name='datail_order'),
    path('list_order/delete/<int:pk>', OrderDelete.as_view()),

    path('list', RepairerL.as_view(), name='list_repair'),
    path('list/<int:pk>', RepaierD.as_view(), name='datail_repair'),
    path('create', RepaierCreate.as_view()),
    path('create/<int:pk>', RepaierUpdate.as_view()),
    path('delete/<int:pk>', RepaierDelete.as_view()),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', BaseRegisterView.as_view(template_name='register.html'), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # для выгрузки картинок из БД в шаблон.
