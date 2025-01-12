from django.urls import path
from mails.views import import_data_to_model

urlpatterns = [
    path('addmails', import_data_to_model, name='addmails'),
]
