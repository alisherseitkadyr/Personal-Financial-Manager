from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Expense, Income
from .services import NotificationService, LowBalanceObserver, HighExpenseObserver, NewTransactionObserver, \
    NegativeBalanceObserver
notification_service = NotificationService()
low_balance_observer = LowBalanceObserver()
high_expense_observer = HighExpenseObserver()
negative_balance_observer=NegativeBalanceObserver()
new_transaction_observer = NewTransactionObserver()

notification_service.register_observer(negative_balance_observer)
notification_service.register_observer(low_balance_observer)
notification_service.register_observer(high_expense_observer)
notification_service.register_observer(new_transaction_observer)

@receiver(post_save, sender=Expense)
@receiver(post_save, sender=Income)
def send_notification(sender, instance, **kwargs):
    notification_service.notify_observers(instance.user)
