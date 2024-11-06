from django import forms
from django.forms import ModelForm

from .models import Expense
from .models import Income
#Form for Date inputs
class DateInput(forms.DateInput):
    input_type = 'date'
# Form for adding expenses
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date']
        widgets = {'date': DateInput()}
# Form for adding incomes
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'amount', 'date']
        widgets = {'date': DateInput()}
