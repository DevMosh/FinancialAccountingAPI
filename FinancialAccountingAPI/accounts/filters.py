from django_filters import rest_framework as filters

from accounts.models import UserExpense, UserIncome


class UserExpenseFilter(filters.FilterSet):
    class Meta:
        model = UserExpense
        fields = "__all__"


class UserIncomeFilter(filters.FilterSet):
    class Meta:
        model = UserIncome
        fields = "__all__"
