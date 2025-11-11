from django import forms

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
