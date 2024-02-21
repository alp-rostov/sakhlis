# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

from .tasks import *
from django.views.generic import ListView
from forms import MyForm


class Home(ListView):
    template_name = 'home.html'
    model = Email
    context_object_name = 'mail_list'

    def get_context_data(self, *args, **kwargs):
        context= super(ListView, self).get_context_data(**kwargs)
        context['form'] = MyForm
        return context



def form_sent(request):
    sent_to_users.delay(news=request.GET.get('news_text'), idlist=request.GET.getlist('id'))
        return JsonResponse({}, status=200)

