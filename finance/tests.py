from django.test import TestCase
from .models import Expense, Income
from .services import BalanceService

from datetime import date

class BalanceServiceTestCase(TestCase):
    def setUp(self):
        # Ensure that 'date' is provided when creating Expense
        Expense.objects.create(amount=100, date=date.today())

    def test_expense_creation(self):
        expense = Expense.objects.first()
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.date, date.today())
class BalanceServiceTestCase(TestCase):

    def setUp(self):
        # Add test data
        Expense.objects.create(amount=100)
        Income.objects.create(amount=200)

    def test_singleton_instance(self):
        # Create two instances of BalanceService
        balance_service1 = BalanceService()
        balance_service2 = BalanceService()

        # Check if both instances are the same
        self.assertIs(balance_service1, balance_service2, "Singleton instances should be the same")

    def test_balance_calculation(self):
        balance_service = BalanceService()

        # Recalculate totals and balance
        balance_service.calculate_totals()

        # Check if balance is calculated correctly
        self.assertEqual(balance_service.get_total_expenses(), 100)
        self.assertEqual(balance_service.get_total_income(), 200)
        self.assertEqual(balance_service.get_balance(), 100)  # 200 - 100 = 100

    def test_home_view(self):
        # Simulate a request to the home view
        response = self.client.get('/home/')

        # Check if the response contains the correct balance values
        self.assertContains(response, 'Total Expenses: 100')
        self.assertContains(response, 'Total Income: 200')
        self.assertContains(response, 'Balance: 100')
