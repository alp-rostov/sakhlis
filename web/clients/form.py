from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, lang='ru', **kwargs):
        self.lang = lang
        langv={'ru':['Имя', 'Телефон'], 'en':['Name', 'Phone'], 'ge':['სახელი', 'ტელეფონი']}
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['customer_name'].label = langv[self.lang][0]
        self.fields['phone'].label = langv[self.lang][1]

    customer_name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "Input your name",
                                      'maxlength': 20}),
        required=True
    )

    phone = forms.CharField(
        label='Phone',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "99512345678",
                                      'type': 'tel',
                                      'maxlength': 16}),
        required=False
    )
    telegram = forms.CharField(
        label='Telegram',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "@telegram",
                                      'maxlength': 26}),
        required=False
    )
    whatsapp = forms.CharField(
        label='Whatsapp',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "99587654321",
                                      'maxlength': 26,
                                      'type': 'tel'}),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ('customer_name', 'phone', 'telegram', 'whatsapp')


class CustomerFormForModal(forms.ModelForm):
    customer_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={"class": "form-control mb-2",
                                      'placeholder': "Name",
                                      'maxlength': 20}),
        required=True
    )
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={"class": "form-control mb-2",
                                      'placeholder': "Phone",
                                      'type': 'tel',
                                      'maxlength': 16}),
        required=False
    )
    telegram = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={"class": "form-control  mb-2",
                                      'placeholder': "Telegram",
                                      'maxlength': 26}),
        required=False
    )
    whatsapp = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={"class": "form-control  mb-2",
                                      'placeholder': "Whatsapp",
                                      'type': 'tel',
                                      'maxlength': 26}),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ('customer_name', 'phone', 'telegram', 'whatsapp')
