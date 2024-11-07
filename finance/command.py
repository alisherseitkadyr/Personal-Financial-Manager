
from .models import Expense, Income, Notification
from .forms import ExpenseForm, IncomeForm
from datetime import date
from django.shortcuts import redirect

class AddExpenseCommand(Command):
    def __init__(self, user, form_data):
        self.user = user
        self.form_data = form_data
        self.expense = None

    def execute(self):
        form = ExpenseForm(self.form_data)
        if form.is_valid():
            self.expense = form.save(commit=False)
            self.expense.user = self.user
            self.expense.date = self.form_data.get('date', date.today())
            self.expense.save()
        return redirect('add_expense')

    def undo(self):
        if self.expense:
            self.expense.delete()


class AddIncomeCommand(Command):
    def __init__(self, user, form_data):
        self.user = user
        self.form_data = form_data
        self.income = None

    def execute(self):
        form = IncomeForm(self.form_data)
        if form.is_valid():
            self.income = form.save(commit=False)
            self.income.user = self.user
            self.income.save()
        return redirect('add_income')

    def undo(self):
        if self.income:
            self.income.delete()


class MarkNotificationReadCommand(Command):
    def __init__(self, user, notification_id):
        self.user = user
        self.notification_id = notification_id
        self.notification = None

    def execute(self):
        self.notification = Notification.objects.get(id=self.notification_id, user=self.user)
        self.notification.is_read = True
        self.notification.save()
        return {'status': 'success'}

    def undo(self):
        if self.notification:
            self.notification.is_read = False
            self.notification.save()
