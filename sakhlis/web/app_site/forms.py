from urllib import request

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class RepairerForm(forms.ModelForm):

    class Meta:
        model = RepairerList
        fields = ['phone', 'city', 'foto']


class OrderForm(forms.ModelForm):
    text_order = forms.CharField(
        label='Текст заказа',
        widget=forms.TextInput(attrs={"class": "md-textarea form-control",
                                     'placeholder': "Опишите задачу", 'maxlength':1500}),
        required=False
        )

    customer_name = forms.CharField(
        label='Ваше имя',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Имя", 'maxlength':50}),
        required=False
    )

    customer_phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Телефон", 'type': 'tel', 'maxlength':16}),
        required=False,

    )

    address_street_app = forms.CharField(
        label='Улица',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Улица", 'maxlength':150}),
        required = False
    )

    address_num = forms.CharField(
        label='Номер дома',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Номер дома", 'maxlength':10}),
        required = False
    )

    class Meta:
        model = OrderList
        fields = ('text_order',
                  'customer_name',
                  'customer_phone',
                  'address_street_app',
                  'address_num',
                                    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.EmailInput(
                                 attrs={"class": "form-control", 'placeholder': "email"}
                                                    ),
                             )
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    username = forms.CharField(label="Логин")
    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2"
                  )


class InvoiceForm(forms.ModelForm):

    service_id = forms.ModelChoiceField(
        label='',
        queryset = Service.objects.all(),
        widget = forms.Select(attrs={'placeholder': "Вид работ" }),

    )
    quantity = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': "Количество", "min": 1, "max": 1000000, 'value': 1}),


    )
    price = forms.DecimalField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': "Цена", "min": 1, "max": 1000000, }),
    )
    class Meta:
        model = Invoice
        fields = ('service_id',   'quantity', 'price')




class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'