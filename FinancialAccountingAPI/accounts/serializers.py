from rest_framework import serializers

from .models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_verified', 'is_superuser', 'balance')


class UsersSerializerFinance(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('balance', )
