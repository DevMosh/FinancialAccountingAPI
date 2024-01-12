from datetime import timedelta, datetime
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User, UserExpense, UserIncome
from .serializers import UsersSerializer, UsersSerializerFinance

from categories.models import Category, CategoryUser
from categories.serializers import CategoriesSerializer


class UsersAPIList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class UserAPICatigories(APIView):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user_profile = CategoryUser.objects.get(user_id=user_id)

        serializer = CategoriesSerializer(user_profile.categories.values('name'), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'pk'


class UserAPIAddCatigories(APIView):
    """ add a category to the user,
            if it does not exist,
            create a new category """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'category_name': openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=['user_id', 'category_name']
        ),
        responses={200: UsersSerializer()},
    )
    def put(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        category_name = request.data.get('category_name')
        category, created = Category.objects.get_or_create(name=category_name)
        user_profile, created = CategoryUser.objects.get_or_create(user_id=user_id)
        user_profile.categories.add(category)
        user_profile.save()

        serializer = CategoriesSerializer(user_profile.categories.values('name'), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes = (IsAuthenticatedOrReadOnly, )


class UserAPIExpense(RetrieveAPIView):
    queryset = UserExpense.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'pk'


class UserAPIAmountOfExpense(APIView):
    def get(self, request, pk, *args, **kwargs):
        """ total expenses for N days """

        user_id = pk
        days = request.query_params.get('days')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=int(days)) if days else end_date

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

        result = UserExpense.objects.filter(
            user=user,
            date__range=(start_date, end_date)
        ).aggregate(Sum('amount'))

        total_expenses = result['amount__sum'] if result['amount__sum'] is not None else Decimal('0.0')

        return Response({
            "total_expense": total_expenses
        }, status=status.HTTP_200_OK)


class UserAPIAddExpense(APIView):
    """ add expense """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                'category_name': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['user_id', 'amount', 'description']
        ),
        responses={200: UsersSerializerFinance()},
    )
    def put(self, request, *args, **kwargs):

        user_id = request.data.get('user_id')
        amount = request.data.get('amount')
        category_name = request.data.get('category_name')
        description = request.data.get('description')

        try:
            user = User.objects.get(pk=user_id)

            if user.balance < Decimal(amount):
                return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.balance -= Decimal(amount)
                user.save()

            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                return Response({"error": f"Category with name '{category_name}' not found"},
                                status=status.HTTP_404_NOT_FOUND)

            expense = UserExpense.objects.create(
                user=user,
                amount=amount,
                category=category,
                description=description
            )

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsersSerializerFinance(user)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


class UserAPIIncome(RetrieveAPIView):
    queryset = UserIncome.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'pk'


class UserAPIAmountOfIncome(APIView):
    """ total incomes for N days """

    def get(self, request, pk, *args, **kwargs):
        user_id = pk
        days = request.query_params.get('days')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=int(days)) if days else end_date

        end_date = datetime.combine(end_date, datetime.max.time())
        start_date = datetime.combine(start_date, datetime.min.time())

        result = UserIncome.objects.filter(
            user=user,
            date__range=(start_date, end_date)
        ).aggregate(Sum('amount'))

        total_incomes = result['amount__sum'] if result['amount__sum'] is not None else Decimal('0.0')

        return Response({
            "total_income": total_incomes
        }, status=status.HTTP_200_OK)


class UserAPIAddIncome(APIView):
    """ Add Incomes """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['user_id', 'amount', 'description']
        ),
        responses={200: UsersSerializerFinance()},
    )
    def put(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        amount = request.data.get('amount')
        description = request.data.get('description')

        try:
            user = User.objects.get(pk=user_id)

            user.balance += Decimal(amount)
            user.save()

            expense = UserIncome.objects.create(
                user=user,
                amount=amount,
                description=description
            )

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsersSerializerFinance(user)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
