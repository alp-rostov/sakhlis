from django import forms
from .models import RepairerList
class RepairerForm(forms.ModelForm):
   class Meta:
       model = RepairerList
       fields = '__all__'