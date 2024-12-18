from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *


urlpatterns = [

path('user/<int:pk>', RepairerDetailInformation.as_view(), name='user'),
]
