from django import forms
from django.forms import ModelForm
from .models import Expense
from .models import Income
from datetime import date

#Form for Date inputs
class DateInput(forms.DateInput):
    input_type = 'date'
# Form for adding expenses
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date']
        widgets = {'date': DateInput()}

    # Make date optional and set default to today
    date = forms.DateField(required=False, initial=date.today)

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'amount', 'date']
        widgets = {'date': DateInput()}
