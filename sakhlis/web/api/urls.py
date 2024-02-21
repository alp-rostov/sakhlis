from django.urls import path

from api.views import ApiStreetView, ApiOrderListCreate

urlpatterns = [
    path('street/', ApiStreetView.as_view()),
    path('stree/', ApiOrderListCreate.as_view()),
]