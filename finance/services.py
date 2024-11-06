from .singleton import Singleton
from django.db.models import Sum
from .models import Expense, Income

class BalanceService(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.total_expenses = None
            self.total_income = None
            self.balance = None
            self.initialized = True

    def calculate_totals(self):
        self.total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        self.total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
        self.balance = self.total_income - self.total_expenses

    def get_total_expenses(self):
        if self.total_expenses is None:
            self.calculate_totals()
        return self.total_expenses

    def get_total_income(self):
        if self.total_income is None:
            self.calculate_totals()
        return self.total_income

    def get_balance(self):
        if self.balance is None:
            self.calculate_totals()
        return self.balance