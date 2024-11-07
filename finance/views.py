from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from datetime import date

from .forms import ExpenseForm, IncomeForm
from .models import Expense, Income, Notification
from .services import BalanceService, InfoNotification, WarningNotification, SuccessNotification
from .services import FinanceFacade

def mark_notification_read(request, notification_id):
    if request.user.is_authenticated:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=403)

# Retrieve all user's expenses
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, '../templates/expense_list.html', {'expenses': expenses})

# Add an expense for a user after submitting form
@login_required
def add_expense(request):
    # Initialize the FinanceFacade
    finance_facade = FinanceFacade()

    # Get unread notifications for the user
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    notification_elements = []

    for notification in notifications:
        if notification.level == "info":
            # Use InfoNotification class for info level notifications
            service = InfoNotification()
        elif notification.level == "warning":
            # Use WarningNotification class for warning level notifications
            service = WarningNotification()
        else:
            # Use SuccessNotification class for success level notifications
            service = SuccessNotification()

        # Generate notification HTML
        notification_elements.append(service.get_notification_html(notification.message, notification.id))

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('date'):
                form.instance.date = date.today()  # Set today's date if no date is provided
            expense = form.save(commit=False)
            expense.user = request.user  # Link expense to the logged-in user
            expense.save()
            finance_facade.notify_on_new_transaction(request.user)  # Notify after transaction
            return redirect('add_expense')
    else:
        form = ExpenseForm()

    return render(request, '../templates/add_expense.html', {'form': form, 'notification_elements': notification_elements})

# Retrieve all user's incomes
@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, '../templates/income_list.html', {'incomes': incomes,})

# Add an income for a user after submitting form
@login_required
def add_income(request):
    # Initialize the FinanceFacade
    finance_facade = FinanceFacade()

    # Get unread notifications for the user
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    notification_elements = []
    for notification in notifications:
        if notification.level == "info":
            service = finance_facade.notification_service.get_notification_html("info", notification.message, notification.id)
        elif notification.level == "warning":
            service = finance_facade.notification_service.get_notification_html("warning", notification.message, notification.id)
        else:
            service = finance_facade.notification_service.get_notification_html("success", notification.message, notification.id)
        notification_elements.append(service)

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Link income to the logged-in user
            income.save()

            # Notify after transaction only once
            if not request.session.get('income_notification_sent', False):  # Check session flag
                finance_facade.notify_on_new_transaction(request.user)  # Notify after transaction
                request.session['income_notification_sent'] = True  # Set flag to avoid repeat notifications

            return redirect('add_income')
    else:
        form = IncomeForm()

    return render(request, '../templates/add_income.html', {'form': form, 'notification_elements': notification_elements})

class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'expense_confirm_delete.html'  # template for confirmation
    success_url = reverse_lazy('expense_list')     # URL to redirect after deletion

class IncomeDeleteView(DeleteView):
    model = Income
    template_name = 'income_confirm_delete.html'  # template for confirmation
    success_url = reverse_lazy('income_list')     # URL to redirect after deletion

# Calculate user's total expenses, income, and balance
@login_required
def home(request):
    finance_facade = FinanceFacade()
    financial_summary = finance_facade.get_financial_summary(request.user)

    return render(request, 'home.html', {
        'total_expenses': financial_summary['total_expenses'],
        'total_income': financial_summary['total_income'],
        'balance': financial_summary['balance'],
    })
