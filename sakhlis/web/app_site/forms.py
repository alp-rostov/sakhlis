from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    text_order = forms.CharField(
        label='Текст заказа',
        widget=forms.TextInput(attrs={"class": "md-textarea form-control",
                                     'placeholder': "Опишите задачу", 'maxlength':1500}),
        required=True
        )

    customer_name = forms.CharField(
        label='Ваше имя',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Имя", 'maxlength':20}),
        required=True
    )

    customer_phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Телефон", 'type': 'tel', 'maxlength':16}),
        required=True,

    )

    customer_telegram = forms.CharField(
        label='Телеграм',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Телеграм", 'maxlength':26}),
        required=False,

    )

    address_street_app = forms.CharField(
        label='Улица',
        widget=forms.TextInput(attrs={"class": "form-control", 'list': 'languages', 'placeholder': "Улица", 'maxlength':40}),
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
                  'customer_telegram',
                  'address_street_app',
                  'address_num',
                                    )




class RepairerForm(forms.ModelForm):

    class Meta:
        model = RepairerList
        fields = ['phone', 'city', 'foto']




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(
                                 attrs={ 'placeholder': "@"}
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
        widget=forms.NumberInput(attrs={'placeholder': "Количество", "min": 1, "max": 10000, 'value': 1}),


    )
    price = forms.DecimalField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': "Цена", "min": 1, "max": 10000, }),
    )
    class Meta:
        model = Invoice
        fields = ('service_id',   'quantity', 'price')


class RepairerForm(forms.ModelForm):

    class Meta:
        model = RepairerList
        fields = ('phone', 'telegram', 'profile', 'city', 'foto')

