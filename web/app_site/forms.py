from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ChoiceField

from .models import *

class ApartmentForm(forms.ModelForm):

    address_city = forms.ChoiceField(
        choices=CITY_CHOICES,

        widget=forms.RadioSelect(
            attrs={"class": ""
            },
        ),
        initial="TB"
    )

    address_street_app = forms.CharField(
        label='Street',
        widget=forms.TextInput(attrs={"class": "form-control", 'list': 'languages', 'placeholder': "Street", 'maxlength':40}),
        required = False
    )

    address_num = forms.CharField(
        label='Appartment',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "App1", 'maxlength':10}),
        required = False
    )

    class Meta:
        model = Apartment
        fields = ('address_city',
                  'address_street_app',
                  'address_num',
                                    )

class OrderForm(forms.ModelForm):
    text_order = forms.CharField(
        label='Order`s message',
        widget=forms.TextInput(attrs={"class": "md-textarea form-control",
                                     'placeholder': "Describe your problem", 'maxlength':1500}),
        required=True
        )

    class Meta:
        model = OrderList
        fields = ('text_order', )

class OrderUpdateForm(forms.ModelForm):
    text_order = forms.CharField(
        label='Order`s message',
        widget=forms.TextInput(attrs={"class": "md-textarea form-control",
                                     'placeholder': "Describe your problem", 'maxlength':1500}),
        required=True
        )

    apartment_id = forms.ModelChoiceField(label='Apartment`s customer', queryset=Apartment.objects.all())
    class Meta:
        model = OrderList
        fields = ('text_order', 'apartment_id', 'customer_id')






class CustomerForm(forms.ModelForm):

    customer_name = forms.CharField(
        label='Your Name',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Username", 'maxlength':20}),
        required=True
    )

    profile = forms.CharField(
        label='About you',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "About you: company, job title, etm", 'maxlength':1500}),
        required=True
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
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Phone", 'type': 'tel', 'maxlength':16}),

    )

    telegram = forms.CharField(
        label='Telegram',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Telegram", 'maxlength':26}),

    )

    class Meta:
        model = UserProfile
        fields = ('customer_name', 'phone', 'telegram', 'profile', 'foto', 'city')



class OrderCustomerForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('customer_name', 'phone', 'telegram')


class OrderForm1(forms.ModelForm):

    class Meta:
        model = OrderList
        fields = '__all__'

class UserRegisterForm(UserCreationForm):

    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={"class": "form-control",
                                      'placeholder': "Login"}),
                              )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control",
                                       'placeholder': "Email"}),
                             )

    group = forms.ChoiceField(
        choices=[('owner','Owner'), ('repairer','Repairer')],

        widget=forms.RadioSelect(
            attrs={"class": ""
            },
        ),
        initial="owner"
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={ "class": "form-control", 'placeholder': "Password"      }, ),
    )
    password2 = forms.CharField(

        widget=forms.PasswordInput(
            attrs={"class": "form-control", 'placeholder': "Password"       }, ),
    )
    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",
                  'group'
                  )


class InvoiceForm(forms.ModelForm):

    service_id = forms.ModelChoiceField(
        label='',
        queryset = Service.objects.all(),
        widget = forms.Select(attrs={'placeholder': "Works`s type" }),

    )
    quantity = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': "Quantity", "min": 1, "max": 10000, 'value': 1}),


    )
    price = forms.DecimalField(
        label='',
        widget=forms.NumberInput(attrs={'placeholder': "Price", "min": 1, "max": 10000, }),
    )
    class Meta:
        model = Invoice
        fields = ('service_id',   'quantity', 'price')
