from django.urls import path
from .views import CityList, City, RepairerList, Repairer

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('', CityList.as_view()),
# path('<int:pk>',  City.as_view()),
path('replist', RepairerList.as_view()),
path('replist/<int:pk>', Repairer.as_view()),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # для выгрузки картинок из БД в шаблон.