from decimal import Decimal

from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import UserIncome, UserExpense


@receiver(post_save, sender=UserIncome)
def create_user_income(sender, instance: UserIncome, created, **kwargs):
    if created:
        instance.user.balance = instance.user.balance + Decimal(instance.amount)
        instance.user.save()


@receiver(post_save, sender=UserExpense)
def create_user_expense(sender, instance: UserExpense, created, **kwargs):
    if created:
        instance.user.balance = instance.user.balance - Decimal(instance.amount)
        instance.user.save()