from django.shortcuts import render
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
