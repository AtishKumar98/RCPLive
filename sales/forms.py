from django import forms
from .models import Report,Sale
from django.forms import ModelForm


CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
)
RESULT_BY = (
    ('#1', 'Transaction'),
    ('#2', 'sales date'),
    
)


class SaleSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    chart_type = forms.ChoiceField(choices =CHART_CHOICES)
    results_by = forms.ChoiceField(choices =RESULT_BY)


class SalesForm(ModelForm):
    class Meta:
        model = Sale
        fields='__all__'


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'remarks', )



