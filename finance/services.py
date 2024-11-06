from .singleton import Singleton
from django.db.models import Sum
from .models import Expense, Income


class BalanceService(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.user_data={}
            self.initialized = True

    def calculate_totals(self,user):
        # Calculate total values for a specified user
        total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        balance = total_income - total_expenses
        # Save calculated values in the user_data dictionary
        self.user_data[user.id] = {
            'total_expenses': total_expenses,
            'total_income': total_income,
            'balance': balance
        }
    def get_total_expenses(self, user):
        if user.id not in self.user_data:
            self.calculate_totals(user)
        return self.user_data[user.id]['total_expenses']

    def get_total_income(self, user):
        if user.id not in self.user_data:
            self.calculate_totals(user)
        return self.user_data[user.id]['total_income']

    def get_balance(self, user):
        if user.id not in self.user_data:
            self.calculate_totals(user)
        return self.user_data[user.id]['balance']

    def reset_user_data(self, user):
        # Clears stored data for a specific user
        if user.id in self.user_data:
            del self.user_data[user.id]
