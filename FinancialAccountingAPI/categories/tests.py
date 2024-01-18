
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from categories.models import Category


class CategoriesApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.category1 = Category.objects.create(name='Test category 1')
        self.category2 = Category.objects.create(name='Test category 2')

    def test_categories_list(self):
        url = reverse('categories-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_category_view(self):
        url = reverse('category-view', kwargs={'pk': self.category1.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_category_delete(self):
        url = reverse('category-delete', kwargs={'pk': self.category1.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_category_update(self):
        url = reverse('category-update', kwargs={'pk': self.category1.pk})
        data = {
            'name': 'Test category edit'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)




