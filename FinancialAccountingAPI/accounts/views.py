from datetime import timedelta, datetime
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User, UserExpense, UserIncome
from .serializers import UsersSerializer, UserExpenseSerializer, UserIncomeSerializer

from categories.models import Category, CategoryUser
from categories.serializers import CategoriesSerializer, CategoriesSerializerUser


class UsersAPIList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


# class UserAPICatigories(RetrieveAPIView, APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CategoriesSerializerUser
#
#     def get_object(self):
#         return CategoryUser.objects.get(user=self.request.user)

class UserAPICatigories(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return Category.objects.filter(categoryuser__user=self.request.user)


class UserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersSerializer

    def get_object(self):
        return self.request.user


class UserAPIAddCatigories(APIView):
    permission_classes = [IsAuthenticated, ]
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


class UserAPIExpense(RetrieveAPIView):
    queryset = UserExpense.objects.all()
    serializer_class = UserExpenseSerializer
    lookup_field = 'pk'


class UserAPIAmountOfExpense(APIView):
    def get(self, request, pk, *args, **kwargs):
        """ total expenses for N days """

        user_id = pk
        days = request.query_params.get('days')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError({"error": "User not found"})

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


class UserExpenseListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserExpenseSerializer
    queryset = UserExpense.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        m = UserExpense.objects.all()
        serializer2 = UserExpenseSerializer(instance=m, many=True)

        return Response(serializer2.data, status=status.HTTP_201_CREATED, headers=headers)


class UserAPIIncome(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserIncomeSerializer

    def get_queryset(self):
        print(self.request.__dict__)
        return UserIncome.objects.filter(user=self.request.user)


class UserAPIAmountOfIncome(APIView):
    """ total incomes for N days """

    def get(self, request, pk, *args, **kwargs):
        user_id = pk
        days = request.query_params.get('days')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError({"error": "User not found"})

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


class UserIncomeListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserIncomeSerializer
    queryset = UserIncome.objects.all()






