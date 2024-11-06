from django import forms
from django.forms import ModelForm
from .models import Expense
from .models import Income
from datetime import date


# Form for adding expenses
class ExpenseForm(forms.ModelForm):
    date= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=date.today())
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date']

class IncomeForm(forms.ModelForm):
    date= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=date.today())
    class Meta:
        model = Income
        fields = ['name', 'amount', 'date']
