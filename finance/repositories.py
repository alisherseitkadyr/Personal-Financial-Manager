# repositories.py

from .models import Expense, Income
from django.db.models import Sum

class ExpenseRepository:
    @staticmethod
    def get_all_expenses():
        return Expense.objects.all()

    @staticmethod
    def add_expense(data):
        expense = Expense(**data)
        expense.save()
        return expense

    @staticmethod
    def get_total_expenses():
        return Expense.objects.aggregate(total=Sum('amount'))['total'] or 0


class IncomeRepository:
    @staticmethod
    def get_all_incomes():
        return Income.objects.all()

    @staticmethod
    def add_income(data):
        income = Income(**data)
        income.save()
        return income

    @staticmethod
    def get_total_income():
        return Income.objects.aggregate(total=Sum('amount'))['total'] or 0
