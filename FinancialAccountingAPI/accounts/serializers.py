
from rest_framework import serializers

from .models import User, UserExpense, UserIncome


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'is_verified', 'is_superuser', 'balance')


class UsersSerializerFinance(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('balance', )


class UserExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserExpense
        fields = ('user', 'amount', 'date', 'category', 'description')


class UserIncomeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserIncome
        fields = ('user', 'amount', 'date', 'description')

