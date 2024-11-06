from django import forms
from django.forms import ModelForm

from .models import Expense
from .models import Income

class DateInput(forms.DateInput):
    input_type = 'date'

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date']
        widgets = {'date': DateInput()}

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'amount', 'date']
        widgets = {'date': DateInput()}
