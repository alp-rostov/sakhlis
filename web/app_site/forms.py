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

    link_location = forms.CharField(
        label='Geo location',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "GoogleMap or other location link", 'maxlength': 300}),
        required=False
    )

    class Meta:
        model = Apartment
        fields = ('address_city',
                  'address_street_app',
                  'address_num', 'link_location')


class ApartentUpdateForm(forms.ModelForm):
    class Meta:
        model = Apartment
        exclude = ["owner"]


class CustomerForm(forms.ModelForm):

    customer_name = forms.CharField(
        label='Your Name',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Username", 'maxlength':20}),
        required=True
    )

    profile = forms.CharField(
        label='About you',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "About you: company, job title, etm", 'maxlength':1500}),
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
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Phone", 'type': 'tel', 'maxlength':16}),
        required=False
    )

    telegram = forms.CharField(
        label='Telegram',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Telegram", 'maxlength':26}),
        required=False
    )
    whatsapp = forms.CharField(
        label='Whatsapp',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Whatsapp", 'maxlength': 26}),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ('customer_name', 'phone', 'telegram', 'whatsapp', 'profile', 'foto', 'city')


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


class OrderCustomerForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('customer_name', 'phone', 'telegram')


class OrderForm(forms.ModelForm):
    text_order = forms.CharField(
        label='Order`s message',
        widget=forms.Textarea(attrs={"class": "md-textarea form-control",
                                     'placeholder': "Describe problems", 'maxlength':1500, 'rows':3, 'cols':10}),
        required=True
        )

    class Meta:
        model = OrderList
        fields = ('text_order', )


class OrderUpdateForm(forms.ModelForm):
    def __init__(self, user):
        super().__init__()
        self.user = UserProfile.objects.get(user=user)
        self.fields['apartment_id'] = forms.ModelChoiceField(label='Apartment`s customer', queryset=Apartment.objects.filter(
            owner=self.user), empty_label="Choose address...")

    # text_order = forms.CharField(
    #     label='Order`s message',
    #     widget=forms.TextInput(attrs={"class": "md-textarea form-control",
    #                                  'placeholder': "Describe your problem", 'maxlength':1500}),
    #     required=True
    #     )
    class Meta:
        model = OrderList
        fields = ('text_order', 'apartment_id')


class OwnerFormOrder(forms.ModelForm):
    def __init__(self, user, app):
        super().__init__()
        self.user=UserProfile.objects.get(user=user)
        self.app=app
        self.fields['apartment_id'] = forms.ModelChoiceField(label='Apartment`s customer', queryset=app, empty_label="Choose address...")
        self.fields['customer_id']= forms.ModelChoiceField(queryset=UserProfile.objects.filter(user=user).only('customer_name'), empty_label=None)


    text_order = forms.CharField(
        label='Order`s message',
        widget=forms.Textarea(attrs={"class": "md-textarea form-control",
                                     'placeholder': "Describe problems", 'maxlength':1500, 'rows':5, 'cols':10}),
        required=True
        )


    class Meta:
        model = OrderList
        fields =('text_order',)


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

