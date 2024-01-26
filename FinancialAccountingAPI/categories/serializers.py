from rest_framework import serializers

from categories.models import Category, CategoryUser


class CategoriesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Category
        fields = ['name', 'user']


class CategoryUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CategoryUser
        fields = '__all__'




