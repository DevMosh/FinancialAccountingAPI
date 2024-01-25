from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UsersAPIList.as_view(), name="users-list"),  # get
    path("user/", views.UserAPIView.as_view(), name="user-view"),  # get

    path("user/categories/", views.UserAPICatigories.as_view(), name="user-categories-list"),  # get, post

    path("user/amount_of_expense/", views.UserAPIAmountOfExpense.as_view(), name="user-amout-of-expense"),  # get
    path("user/expenses/", views.UserExpenseListView.as_view(), name="user-add-expense"),  # get, post

    path("user/amount_of_income/", views.UserAPIAmountOfIncome.as_view(), name="user-amout-of-income"),  # get
    path("user/incomes/", views.UserIncomeListView.as_view(), name="user-add-income"),  # get, post
]