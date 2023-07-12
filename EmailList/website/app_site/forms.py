from django import forms

class MyForm(forms.Form):
    news_text = forms.CharField(label="",
                             widget=forms.Textarea(
                                 attrs={"class": "form-control", 'placeholder': "TEXT"}
                             ),
                             )