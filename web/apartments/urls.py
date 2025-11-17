from billiard.sharedctypes import template
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
path('updatephotoapartment/<int:pk>', ApartmentPhotoUpdate.as_view(), name='updatephotoapartment'),
path('updateapartment/<int:pk>', ApartmentUpdate.as_view(), name='updateapartment',),

# path('createphotoapartment/<int:pk>', ApartmentPhotoCreate.as_view(), name='createphotoapartment'),

]