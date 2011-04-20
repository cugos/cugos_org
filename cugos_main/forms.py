from django.forms import ModelForm
from cugos_main.models import *
from django.forms.util import ValidationError
from django import forms

class AddFlaw(ModelForm):
    geometry = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Flaws
        exclude = ('popularity')

    def clean_geometry(self):
        if not self.cleaned_data.get('geometry'):
          raise ValidationError("Please plot your flaw before submitting form.")
        return self.cleaned_data['geometry']
        
        
