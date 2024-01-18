from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

# Create your tests here.

from rest_framework.test import APITestCase, APIClient

from accounts.models import User, UserExpense, UserIncome
from categories.models import Category, CategoryUser


class UsersApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(email='test@gmail.com', username='root', password='1234', balance=Decimal(1000))
        self.user2 = User.objects.create_user(email='test1@gmail.com', username='root1', password='1234', balance=Decimal(1000))
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")

        user_profile = CategoryUser.objects.create(user_id=self.user1.pk)
        user_profile.categories.add(self.category1.id)

        self.days = 7

        UserExpense.objects.create(
            user=self.user1,
            amount=Decimal(33),
            category=self.category1,
            description=None
        )

        UserIncome.objects.create(
            user=self.user1,
            amount=Decimal(2),
            description=None
        )

    def test_users_list(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse(r'users-list')

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_view(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse(r'user-view')

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_categories_list(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse(r'user-categories-list', kwargs={'pk': self.user1.pk})

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_add_categories_list_auth(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse('user-add-categories-list')
        json = {
            'user_id': self.user1.id,
            'category_name': 'Category 1'
        }
        response = self.client.put(url, data=json)

        self.assertEqual(200, response.status_code)

    def test_user_add_categories_list_no_auth(self):
        # self.client.force_authenticate(user=None)

        url = reverse('user-add-categories-list')
        json = {
            'user_id': self.user1.id,
            'category_name': 'Category 1'
        }
        response = self.client.put(url, data=json)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_user_expense_list(self):
        url = reverse(r'user-expense-list', kwargs={'pk': self.user1.pk})

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_amout_of_expense(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse(r'user-amout-of-expense', kwargs={'pk': self.user1.pk, 'days': self.days})

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_add_expense_no_auth(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse(r'user-add-expense')

        data = {
            "amount": 1.00,
            "category": self.category1.id,
            "description": 'Description 2'
        }

        print(data)

        response = self.client.post(url, data=data)
        print(response.data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_user_income_list(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse(r'user-income-list', kwargs={'pk': self.user1.pk})

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_amount_of_income(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse(r'user-amout-of-income', kwargs={'pk': self.user1.pk, 'days': self.days})

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_add_income_auth(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse(r'user-add-income')

        data = {
            "amount": 1.00,
            "description": 'Description 2'
        }

        print(data)

        response = self.client.post(url, data=data)
        print(response.data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_user_add_income_no_auth(self):
        self.client.force_authenticate(user=None)

        url = reverse(r'user-add-income')

        data = {
            "amount": 1.00,
            "description": 'Description 2'
        }

        print(data)

        response = self.client.post(url, data=data)
        print(response.data)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
