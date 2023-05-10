from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import DateTimeInput

from .models import RepairerList, OrderList


class RepairerForm(forms.ModelForm):
    class Meta:
        model = RepairerList
        fields = '__all__'


class OrderForm(forms.ModelForm):
    text_order = forms.CharField(
        label='Текст заказа',
        widget=forms.Textarea(attrs={"class": "md-textarea form-control", 'placeholder': "Опишите задачу", 'rows': '2'})
        )

    customer_name = forms.CharField(
        label='Ваше имя',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Ваше имя"})
    )

    customer_phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Телефон", 'type': 'tel'})
    )

    address_street_app = forms.CharField(
        label='Улица',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Улица"})
    )

    address_num = forms.CharField(
        label='Номер дома',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Номер дома"})
    )

    time_out = forms.DateTimeField(
        label='Дата выполнения',
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False

    )

    class Meta:
        model = OrderList
        fields = ('text_order',
                  'customer_name',
                  'customer_phone',
                  'address_street_app',
                  'address_num',
                  'repairer_id',
                  'price',
                  'time_out'
                  )


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",
                  )