from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Category
from .serializers import CategoriesSerializer


class CategoryAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
