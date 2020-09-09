from django import forms
from django.core.validators import validate_integer
from .models import Steps


class StepsForm(forms.ModelForm):

    class Meta:
        model = Steps
        fields = ('steps', 'created_at',)
        widgets = {
            'steps': forms.NumberInput(attrs={'class': 'form-control', 'placefolder': 'Your activity must be between 1 - 50000','min': '1', 'max': '50000', 'required':'true' , 'type': 'number'}),
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'})
        }
        

class SearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}))
    date_to=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}))
