from django.shortcuts import render, redirect
from .forms import ExpenseForm, IncomeForm
from .models import Expense, Income
from .services import BalanceService
from datetime import date


def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Ensure that 'date' is provided or default to today's date
            if not form.cleaned_data.get('date'):
                form.instance.date = date.today()  # Set today's date if no date is provided

            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})


def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'income_list.html', {'incomes': incomes})


def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})


def home(request):
    balance_service = BalanceService()
    print(f"BalanceService instance ID: {id(balance_service)}")  # Print the instance ID

    total_expenses = balance_service.get_total_expenses()
    total_income = balance_service.get_total_income()
    balance = balance_service.get_balance()

    return render(request, 'home.html', {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'balance': balance,
    })

