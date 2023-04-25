from django.urls import path
from .views import RepairerL

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RepairerL.as_view()),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # для выгрузки картинок из БД в шаблон.
