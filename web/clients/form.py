from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class CustomerForm(forms.ModelForm):
    customer_name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "Name",
                                      'maxlength': 20}),
        required=True
    )
    profile = forms.CharField(
        label='Additional information:',
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   'placeholder': "About company, job title, etm",
                   'maxlength': 1500}),
        required=False
    )
    city = forms.ChoiceField(
        choices=CITY_CHOICES,

        widget=forms.RadioSelect(
            attrs={"class": ""
                   },
        ),
        initial="TB"
    )
    phone = forms.CharField(
        label='Phone',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "Phone",
                                      'type': 'tel',
                                      'maxlength': 16}),
        required=False
    )
    telegram = forms.CharField(
        label='Telegram',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "Telegram",
                                      'maxlength': 26}),
        required=False
    )
    whatsapp = forms.CharField(
        label='Whatsapp',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "Whatsapp",
                                      'maxlength': 26,
                                      'type': 'tel'}),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ('customer_name', 'phone', 'telegram', 'whatsapp', 'profile', 'city')


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
