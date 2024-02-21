from django.urls import path

from api.views import YourView

urlpatterns = [
    path('street/', YourView.as_view(), name='street'),

]