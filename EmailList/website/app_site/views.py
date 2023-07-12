# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, FormView
from .tasks import *
from .forms import MyForm


class Home(FormView):
    template_name = 'home.html'
    form_class = MyForm

def form_sent(request, *args, **kwargs):
    sent_to_users.delay(news=request.POST['news_text'])
    return JsonResponse()