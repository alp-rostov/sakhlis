from django.contrib.auth.forms import UserCreationForm
from django import forms

from clients.models import UserProfile
from .constants import CITY_CHOICES, APART_CHOICES
from .models import *

class ApartmentFormOwner(forms.Form):
    apartment_id = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, person, *args, **kwargs):
        self.person=person
        super(ApartmentFormOwner, self).__init__(*args, **kwargs)
        self.fields['apartment_id'].choices = [(x.pk, f'{x.name} | {x.address_street_app} {x.address_num}') for x in Apartment.objects.filter(owner=self.person).order_by('name','address_street_app')]


class ApartmentForm(forms.ModelForm):

    address_city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.RadioSelect(attrs={"class": ""},),
        initial="TB"
    )
    address_street_app = forms.CharField(
        label='Street',
        widget=forms.TextInput(
            attrs={"class": "form-control", 'list': 'languages', 'placeholder': 'ქუჩა / Street', 'maxlength': 40}),
        required=False
    )
    address_num = forms.CharField(
        label='Apartment (number, entrance, floor etc.)',
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "ბინა / Apartment", 'maxlength': 150}),
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

    type = forms.ChoiceField(
        choices=APART_CHOICES,
        label='Type of apartment',
        widget=forms.Select(attrs={"class": "form-control"},),
        initial="FL"
    )

    class Meta:
        model = Apartment
        exclude = ["owner"]


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

class SendOffer(forms.Form):
    username = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={"class": "form-control mb-2", 'placeholder': "Login"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control mb-2", 'placeholder': "Email"}),
    )
