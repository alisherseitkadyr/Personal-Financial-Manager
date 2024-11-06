# services.py

from .repositories import ExpenseRepository, IncomeRepository

class FinanceService:
    def __init__(self):
        self.expense_repository = ExpenseRepository
        self.income_repository = IncomeRepository

    def list_expenses(self):
        return self.expense_repository.get_all_expenses()

    def add_expense(self, data):
        return self.expense_repository.add_expense(data)

    def list_incomes(self):
        return self.income_repository.get_all_incomes()

    def add_income(self, data):
        return self.income_repository.add_income(data)

    def calculate_totals(self):
        total_expenses = self.expense_repository.get_total_expenses()
        total_income = self.income_repository.get_total_income()
        balance = total_income - total_expenses
        return {
            'total_expenses': total_expenses,
            'total_income': total_income,
            'balance': balance
        }
