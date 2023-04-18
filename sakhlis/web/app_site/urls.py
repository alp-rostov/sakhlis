from django.urls import path
from .views import RepairerL, RepaierD, Repaier_create

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('', RepairerL.as_view()),
path('<int:pk>', RepaierD.as_view(), name='datail_repair'),
path('create', Repaier_create.as_view()),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # для выгрузки картинок из БД в шаблон.