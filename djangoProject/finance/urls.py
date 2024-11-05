# finance/urls.py

from django.urls import path
from .views import expense_list, add_expense, income_list, add_income, home  # Импортируйте функцию home

urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('expenses/', expense_list, name='expense_list'),  # Список расходов
    path('expenses/add/', add_expense, name='add_expense'),  # Добавление расхода
    path('incomes/', income_list, name='income_list'),  # Список доходов
    path('incomes/add/', add_income, name='add_income'),  # Добавление дохода
]

