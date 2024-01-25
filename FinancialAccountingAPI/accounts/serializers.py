import datetime
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.request import Request

from .models import User, UserExpense, UserIncome


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'is_verified', 'is_superuser', 'balance')


class UserExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserExpense
        fields = '__all__'


class UserIncomeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserIncome
        fields = "__all__"


class UserTotalExpenseSerializer(serializers.ModelSerializer):
    total_expense = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['total_expense']

    def get_total_income(self, obj):
        days = int(self.context['request'].query_params.get('days'))
        date = datetime.datetime.now() - datetime.timedelta(days=days)
        obj: User
        return obj.userincome_set.filter(date__gte=date).aggregate(total_income=Sum('amount'))['total_expense'] or 0


class UserTotalIncomeSerializer(serializers.ModelSerializer):
    total_income = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['total_income']

    def get_total_income(self, obj):
        days = int(self.context['request'].query_params.get('days'))
        date = datetime.datetime.now() - datetime.timedelta(days=days)
        obj: User
        return obj.userincome_set.filter(date__gte=date).aggregate(total_income=Sum('amount'))['total_income'] or 0
