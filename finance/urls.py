from django.urls import path
from .views import expense_list, add_expense, income_list, add_income, home

urlpatterns = [
    path('', home, name='home'),  # Home page path
    path('expenses/', expense_list, name='expense_list'),  # Expenses list path
    path('expenses/add/', add_expense, name='add_expense'),  # Add expenses page path
    path('incomes/', income_list, name='income_list'),  # Incomes list path
    path('incomes/add/', add_income, name='add_income'),  # Add incomes page path
]

