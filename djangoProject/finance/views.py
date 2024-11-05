from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense, Income
from .forms import IncomeForm
from django.db.models import Sum
from finance import views  # Замените 'myapp' на название вашего приложения


def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'finance/expense_list.html', {'expenses': expenses})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'finance/add_expense.html', {'form': form})

def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'finance/income_list.html', {'incomes': incomes})

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'finance/add_income.html', {'form': form})

def home(request):
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expenses

    return render(request, 'finance/home.html', {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'balance': balance,
    })
