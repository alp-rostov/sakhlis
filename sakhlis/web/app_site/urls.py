from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import RepairerL, RepaierD, RepaierCreate, RepaierUpdate, RepaierDelete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RepairerL.as_view(), name='list_repair'),
    path('<int:pk>', RepaierD.as_view(), name='datail_repair'),
    path('create', RepaierCreate.as_view()),
    path('create/<int:pk>', RepaierUpdate.as_view()),
    path('delete/<int:pk>', RepaierDelete.as_view()),
    path('login/', LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # для выгрузки картинок из БД в шаблон.
