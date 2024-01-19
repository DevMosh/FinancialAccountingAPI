from rest_framework import generics

from .models import Category
from .serializers import CategoriesSerializer


class CategoryAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'pk'