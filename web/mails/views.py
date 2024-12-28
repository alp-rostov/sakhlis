from django.shortcuts import render, redirect
from django.views.generic import FormView

from app_site.forms import SendOffer
from app_site.tasks import send_email
from mails.models import Mail

import pandas as pd


def import_data_to_model(request, **kwargs):
    """import data into model from emails.xlsx"""
    # Client.objects.all().delete()
    excel_data = pd.read_excel('emails.xlsx')
    data = pd.DataFrame(excel_data, columns=['emails'])
    for i in data['emails']:
        b = Mail(mail=i, flag=False)
        b.save()


class SendOffer(FormView):
    template_name = 'offers.html'
    form_class = SendOffer
    def post(self, formset, **kwargs):

        send_email(self.request.POST['email'],
                   'Repair services in Georgia',
                   'emails/mail-offer.html',
                   {'name': self.request.POST['username']}
                   )
        return redirect('sendoffer')

