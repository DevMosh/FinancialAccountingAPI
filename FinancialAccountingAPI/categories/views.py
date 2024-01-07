
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

from categories.models import Category
from .serializers import CategoriesSerializer


# все категории
class CategoryAPIList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


# название категории
class CategoryAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'pk'


# изменение названия категории
class CategoryAPIUpdate(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'pk'


# удаление категории
class CategoryAPIDelete(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'pk'