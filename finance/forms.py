from django import forms
from .models import Expense
from .models import Income
from django import forms
from .models import Expense
from datetime import date

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date']

    # Make date optional and set default to today
    date = forms.DateField(required=False, initial=date.today)

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'amount', 'date']
