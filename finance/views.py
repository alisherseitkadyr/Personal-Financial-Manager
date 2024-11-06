

from django.shortcuts import render, redirect
from .forms import ExpenseForm, IncomeForm
from .services import FinanceService

finance_service = FinanceService()

def expense_list(request):
    expenses = finance_service.list_expenses()
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            finance_service.add_expense(form.cleaned_data)
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

def income_list(request):
    incomes = finance_service.list_incomes()
    return render(request, 'expenses/income_list.html', {'incomes': incomes})

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            finance_service.add_income(form.cleaned_data)
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'expenses/add_income.html', {'form': form})

def home(request):
    totals = finance_service.calculate_totals()
    return render(request, 'expenses/home.html', totals)
