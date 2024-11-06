from django.urls import path
from .views import expense_list, add_expense, income_list, add_income, home  # Import views correctly

urlpatterns = [
    path('', home, name='home'),
    path('expenses/', expense_list, name='expense_list'),
    path('expenses/add/', add_expense, name='add_expense'),
    path('incomes/', income_list, name='income_list'),
    path('incomes/add/', add_income, name='add_income'),
]
