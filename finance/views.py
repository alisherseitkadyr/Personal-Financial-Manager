from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ExpenseForm, IncomeForm
from .models import Expense, Income
from .services import BalanceService
from datetime import date
# Retrieve all user's expenses
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, '../templates/expense_list.html', {'expenses': expenses})
# Add an expense for a user after submitting form
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Ensure that 'date' is provided or default to today's date
            if not form.cleaned_data.get('date'):
                form.instance.date = date.today()  # Set today's date if no date is provided
            expense = form.save(commit=False)
            expense.user = request.user  # Link expense to the logged-in user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, '../templates/add_expense.html', {'form': form})
#Retrieve all user's incomes
@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, '../templates/income_list.html', {'incomes': incomes})
# Add an income for a user after submitting form
@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Link income to the logged-in user
            income.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, '../templates/add_income.html', {'form': form})
# Calculate user's total expenses, income and balance
@login_required
def home(request):
    balance_service = BalanceService()
    print(f"BalanceService instance ID: {id(balance_service)}")  # Print the instance ID
    # Update general info
    balance_service.calculate_totals(request.user)
    total_expenses = balance_service.get_total_expenses(request.user)
    total_income = balance_service.get_total_income(request.user)
    balance = balance_service.get_balance(request.user)

    return render(request, 'home.html', {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'balance': balance,
    })
