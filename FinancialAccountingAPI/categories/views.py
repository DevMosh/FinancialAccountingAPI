from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

from .models import Category
from .serializers import CategoriesSerializer


# class NotEditPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return True
#
#     def has_object_permission(self, request, view, obj: Category) -> bool:
#         print(obj.categoryuser_set.f)
#         return True

# все категории
class CategoryAPIList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = [NotEditPermission, ]


# название категории
class CategoryAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'pk'
    # permission_classes = [NotEditPermission, ]


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