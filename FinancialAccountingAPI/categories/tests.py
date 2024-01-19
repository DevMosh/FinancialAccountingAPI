from rest_framework import status
from rest_framework import test
from django.urls import reverse

from categories.models import Category


class CategoriesApiTests(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient()

        self.category1 = Category.objects.create(name='Test category 1')
        self.category2 = Category.objects.create(name='Test category 2')

    def test_categories_list(self):
        url = reverse('categories:category-api', kwargs={'pk': self.category1.id})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_category_view(self):
        url = reverse('categories:category-api', kwargs={'pk': self.category1.pk})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_category_delete(self):
        url = reverse('categories:category-api', kwargs={'pk': self.category1.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_category_update(self):
        url = reverse('categories:category-api', kwargs={'pk': self.category1.pk})
        data = {
            'name': 'Test category edit'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)




