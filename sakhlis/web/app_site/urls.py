from django.urls import path
from .views import CityList, City

urlpatterns = [
path('', CityList.as_view()),
path('<int:pk>',  City.as_view()),

]