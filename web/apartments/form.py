from django import forms
from app_site.constants import CITY_CHOICES, APART_CHOICES

from .models import ApartmentPhoto, Apartment


class ApartmentFormAddPhoto(forms.ModelForm):
    id_apartments = forms.ModelChoiceField(
        empty_label=None,
        label='Apartment',
        widget=forms.Select(attrs={"class": "md-textarea form-control", }),
        queryset=Apartment.objects.none()
    )

    class Meta:
        model = ApartmentPhoto
        fields = ('id_apartments', 'photo')


class ApartmentFormUpdate(forms.ModelForm):
    id_apartments = forms.ModelChoiceField(
        empty_label=None,
        label='Apartment',
        widget=forms.Select(attrs={"class": "md-textarea form-control", }),
        queryset=Apartment.objects.none()
    )
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': 'Name', 'maxlength': 140}),
        required=False
    )
    type = forms.ChoiceField(
        choices=APART_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"},),

    )
    address_city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.RadioSelect(attrs={"class": ""},),
        initial="TB"
    )
    address_street_app = forms.CharField(
        label='Street',
        widget=forms.TextInput(
            attrs={"class": "form-control", 'placeholder': 'ქუჩა / Street', 'maxlength': 40}),
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
        fields = ('id_apartments',
                  'name',
                  'type',
                  'address_city',
                  'address_street_app',
                  'address_num',
                  'link_location')
