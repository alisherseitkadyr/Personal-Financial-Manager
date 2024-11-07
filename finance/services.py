from .singleton import Singleton
from django.db.models import Sum
from .models import Expense, Income, Notification


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

class NotificationService(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.observers=[]
            self.initialized = True
    def register_observer(self, observer):
        self.observers.append(observer)
    def notify_observers(self,user):
        for observer in self.observers:
            observer.update(user)

class InfoNotification(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def get_notification_html(self, message,id):
        return f'<div class="alert alert-info" data-id={id}>{message}</div>'
    def create_notification(self, message,user):
        # Create and save a new notification in the database
        notification = Notification.objects.create(
            user=user,
            message=message,
            level='info'
        )
        return notification

class WarningNotification(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def get_notification_html(self, message,id):
        return f'<div class="alert alert-warning "data-id={id}>{message}</div>'
    def create_notification(self, message,user):
        # Create and save a new notification in the database
        notification = Notification.objects.create(
            user=user,
            message=message,
            level='warning'
        )
        return notification
class SuccessNotification(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def get_notification_html(self, message,id):
        return f'<div class="alert alert-success" data-id={id}>{message}</div>'
    def create_notification(self, message,user):
        # Create and save a new notification in the database
        notification = Notification.objects.create(
            user=user,
            message=message,
            level='success'
        )
        return notification
class LowBalanceObserver(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def update(self,user):
        notification_gen=WarningNotification()
        balance_service = BalanceService()
        balance=balance_service.get_balance(user)
        if balance>0 and user.balance<500:
            notification_gen.create_notification("Your balance is lower than 500",user)
class NegativeBalanceObserver(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def update(self,user):
        notification_gen = WarningNotification()
        balance_service = BalanceService()
        balance=balance_service.get_balance(user)
        if balance<0:
            notification_gen.create_notification("Negative Balance - Expenses are above your income", user)
class HighExpenseObserver(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def update(self,user):
        notification_gen = InfoNotification()
        balance_service = BalanceService()
        total_expenses=balance_service.get_total_expenses(user)
        if total_expenses>5000000:
            notification_gen.create_notification("Your expenses are above 5000000", user)
class NewTransactionObserver(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def update(self,user):
        notification_gen = SuccessNotification()
        notification_gen.create_notification("Transaction added successfully", user)

