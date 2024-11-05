from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import *

class ApartmentFormOwner(forms.Form):
    apartment_id = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, person, *args, **kwargs):
        self.person=person
        super(ApartmentFormOwner, self).__init__(*args, **kwargs)
        self.fields['apartment_id'].choices = [(x.pk, x.address_street_app) for x in Apartment.objects.filter(owner=self.person)]


class ApartmentForm(forms.ModelForm):
    address_city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.RadioSelect(attrs={"class": ""},),
        initial="TB"
    )
    address_street_app = forms.CharField(
        label='Street',
        widget=forms.TextInput(
            attrs={"class": "form-control", 'list': 'languages', 'placeholder': "Street", 'maxlength': 40}),
        required=False
    )
    address_num = forms.CharField(
        label='Appartment',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Apartment", 'maxlength': 10}),
        required=False
    )
    notes = forms.CharField(
        label='Note(entrance, floor, apartment, door code, etc. )',
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': "entrance, floor, door code, etc.", 'maxlength': 40}),
        required=False
    )

    link_location = forms.CharField(
        label='Geo location',
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': "GoogleMap or other location link", 'maxlength': 300}),
        required=False
    )

    class Meta:
        model = Apartment
        fields = ('address_city',
                  'address_street_app',
                  'address_num', 'link_location')


class ApartentUpdateForm(ApartmentForm, forms.ModelForm):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "", 'maxlength': 40}),
        required=False
    )
    notes = forms.CharField(
        label='Note',
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': "Additional information", 'maxlength': 40}),
        required=False
    )
    type = forms.ChoiceField(
        choices=APART_CHOICES,
        label='Type of apartment',
        widget=forms.Select(attrs={"class": "form-control"},),
        initial="FL"
    )

    class Meta:
        model = Apartment
        exclude = ["owner"]


class CustomerForm(forms.ModelForm):
    customer_name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Username", 'maxlength': 20}),
        required=True
    )
    profile = forms.CharField(
        label='Additional information:',
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': "About company, job title, etm", 'maxlength': 1500}),
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
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Phone", 'type': 'tel', 'maxlength': 16}),
        required=False
    )
    telegram = forms.CharField(
        label='Telegram',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Telegram", 'maxlength': 26}),
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
        queryset=Service.objects.all(),
        widget=forms.Select(attrs={'placeholder': "Works`s type"}),
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
        fields = ('service_id', 'quantity', 'price')


class OrderCustomerForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('customer_name', 'phone', 'telegram', 'whatsapp')



class OrderForm(forms.ModelForm):
    text_order = forms.CharField(
        label='Order`s message',
        widget=forms.Textarea(attrs={"class": "md-textarea form-control",
                                     'placeholder': "Describe problems", 'maxlength': 1500, 'rows': 3, 'cols': 10}),
        required=True
    )

    class Meta:
        model = OrderList
        fields = ('text_order',)


class OrderUpdateForm(forms.ModelForm):
    repairer_id = forms.ModelChoiceField(
        label='Handyman',
        widget=forms.Select(attrs={"class": "md-textarea form-control", }),
        queryset=User.objects.all()
    )
    order_status = forms.ChoiceField(
        label='Order`s status',
        widget=forms.Select(attrs={"class": "md-textarea form-control", }),
        choices=ORDER_STATUS
    )
    text_order = forms.CharField(
        label='Order`s message',
        widget=forms.TextInput(attrs={"class": "md-textarea form-control",
                                      'placeholder': "Describe your problem", 'maxlength': 1500}),
    )

    class Meta:
        model = OrderList
        fields = ('repairer_id', 'order_status', 'text_order')


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={"class": "form-control mb-2", 'placeholder': "Login"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control mb-2", 'placeholder': "Email"}),
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-2", 'placeholder': "Password"}, ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-2", 'placeholder': "Password"}, ),
    )

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",
                  )
