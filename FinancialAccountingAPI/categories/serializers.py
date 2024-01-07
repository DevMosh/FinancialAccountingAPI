from rest_framework import serializers

from categories.models import Category, CategoryUser


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class CategoriesSerializerUser(serializers.ModelSerializer):
    class Meta:
        model = CategoryUser
        fields = ('categories', )