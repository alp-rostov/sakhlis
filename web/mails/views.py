from django.shortcuts import render

from mails.models import Client


def aaa(request):
    # Client.objects.all().delete()
    import pandas as pd
    excel_data = pd.read_excel('emails.xlsx')
    data = pd.DataFrame(excel_data, columns=['emails'])
    for i in data['emails']:
        b = Client(mail=i, flag=False)
        b.save()

# Create your views here.
