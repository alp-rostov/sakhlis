from django import forms
from .models import Repairer
class RepairerForm(forms.ModelForm):
   class Meta:
       model = Repairer
       fields = ['name', 's_name', 'phone', 'city', 'email',
                 'foto']