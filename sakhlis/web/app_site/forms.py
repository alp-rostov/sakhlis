from django import forms
from .models import RepairerList
class RepairerForm(forms.ModelForm):
   class Meta:
       model = RepairerList
       fields = ['name', 's_name', 'phone', 'city', 'email',
                 'foto']