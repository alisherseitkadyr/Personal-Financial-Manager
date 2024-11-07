from django.urls import path
from .views import expense_list, add_expense, income_list, add_income, home, mark_notification_read, ExpenseDeleteView, \
    IncomeDeleteView

urlpatterns = [
    path('', home, name='home'),  # Home page path
    path('expenses/', expense_list, name='expense_list'),  # Expenses list path
    path('expenses/add/', add_expense, name='add_expense'),  # Add expenses page path
    path('incomes/', income_list, name='income_list'),  # Incomes list path
    path('incomes/add/', add_income, name='add_income'),  # Add incomes page path
path('notifications/mark-read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
path('expense/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
    path('income/<int:pk>/delete/', IncomeDeleteView.as_view(), name='income_delete'),
]

