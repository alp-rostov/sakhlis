from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', aaa(), name='home'),]
