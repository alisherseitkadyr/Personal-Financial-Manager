from .singleton import Singleton
from django.db.models import Sum
from .models import Expense, Income, Notification


# BalanceService с использованием Singleton
class BalanceService(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.user_data = {}
            self.initialized = True

    def calculate_totals(self, user):
        total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        balance = total_income - total_expenses
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
        if user.id in self.user_data:
            del self.user_data[user.id]


# NotificationService с использованием Singleton и паттерна Наблюдатель
class NotificationService(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.observers = []
            self.initialized = True

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, user):
        for observer in self.observers:
            observer.update(user)

    def get_notification_html(self, level, message, notification_id):
        # Используем соответствующий класс уведомлений
        if level == "info":
            notification = InfoNotification()
        elif level == "warning":
            notification = WarningNotification()
        else:
            notification = SuccessNotification()

        return notification.get_notification_html(message, notification_id)


# Классы для различных типов уведомлений
class InfoNotification(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def get_notification_html(self, message, id):
        return f'<div class="alert alert-info" data-id={id}>{message}</div>'

    def create_notification(self, message, user):
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

    def get_notification_html(self, message, id):
        return f'<div class="alert alert-warning" data-id={id}>{message}</div>'

    def create_notification(self, message, user):
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

    def get_notification_html(self, message, id):
        return f'<div class="alert alert-success" data-id={id}>{message}</div>'

    def create_notification(self, message, user):
        notification = Notification.objects.create(
            user=user,
            message=message,
            level='success'
        )
        return notification


# Классы наблюдателей для различных уведомлений
class LowBalanceObserver(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def update(self, user):
        notification_gen = WarningNotification()
        balance_service = BalanceService()
        balance = balance_service.get_balance(user)
        if balance > 0 and balance < 500:
            notification_gen.create_notification("Your balance is lower than 500", user)


class NegativeBalanceObserver(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def update(self, user):
        notification_gen = WarningNotification()
        balance_service = BalanceService()
        balance = balance_service.get_balance(user)
        if balance < 0:
            notification_gen.create_notification("Negative Balance - Expenses are above your income", user)


class HighExpenseObserver(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def update(self, user):
        notification_gen = InfoNotification()
        balance_service = BalanceService()
        total_expenses = balance_service.get_total_expenses(user)
        if total_expenses > 5000000:
            notification_gen.create_notification("Your expenses are above 5000000", user)


class NewTransactionObserver(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def update(self, user):
        # Проверяем, отправлялось ли уведомление
        notification_check = Notification.objects.filter(
            user=user,
            message="Transaction added successfully"
        )

        # Если уведомление еще не было отправлено
        if not notification_check.exists():
            notification_gen = SuccessNotification()
            notification_gen.create_notification("Transaction added successfully", user)


# Реализация FinanceFacade
class FinanceFacade:
    def __init__(self):
        self.balance_service = BalanceService()
        self.notification_service = NotificationService()
        self.notification_service.register_observer(LowBalanceObserver())
        self.notification_service.register_observer(NegativeBalanceObserver())
        self.notification_service.register_observer(HighExpenseObserver())
        self.notification_service.register_observer(NewTransactionObserver())

    def get_financial_summary(self, user):
        self.balance_service.calculate_totals(user)
        total_expenses = self.balance_service.get_total_expenses(user)
        total_income = self.balance_service.get_total_income(user)
        balance = self.balance_service.get_balance(user)
        return {
            'total_expenses': total_expenses,
            'total_income': total_income,
            'balance': balance
        }

    def notify_on_new_transaction(self, user):
        self.notification_service.notify_observers(user)

