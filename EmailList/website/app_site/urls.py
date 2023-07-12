from django.conf.urls import url

from views import *


urlpatterns = [
    url('sent', form_sent),
    url('', Home.as_view()),
]

