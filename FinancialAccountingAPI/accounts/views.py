from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .filters import UserExpenseFilter
from .models import User, UserExpense, UserIncome
from .serializers import UsersSerializer, UserExpenseSerializer, UserIncomeSerializer, UserTotalIncomeSerializer

from categories.models import Category
from categories.serializers import CategoriesSerializer, CategoryUserSerializer


class UsersAPIList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


# class UserAPICatigories(ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CategoriesSerializer
#
#     def get_queryset(self):
#         return Category.objects.filter(categoryuser__user=self.request.user)


class UserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersSerializer

    def get_object(self):
        return self.request.user


class UserAPICatigories(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CategoriesSerializer

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
    def post(self, request):
        category = Category.objects.filter(name=request.data['name'])
        if category.exists():
            self.request.user.categories.add(category.first().pk)
        print(self.request.user)
        return super(UserAPICatigories, self).post(request)


class CategoryUserCreateView(ListCreateAPIView):
    """ add a category to the user """

    permission_classes = [IsAuthenticated, ]
    serializer_class = CategoryUserSerializer

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)
        return queryset





class UserAPIExpense(RetrieveAPIView):
    queryset = UserExpense.objects.all()
    serializer_class = UserExpenseSerializer
    lookup_field = 'pk'


class UserAPIAmountOfExpense(APIView):
    """ total expenses for N days """
    permission_classes = [IsAuthenticated]
    serializer_class = UserTotalIncomeSerializer

    def get_object(self):
        return self.request.user


class UserExpenseListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserExpenseSerializer
    queryset = UserExpense.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = UserExpenseFilter

    def create(self, request, *args, **kwargs):
        super(UserExpenseListView, self).create(request, *args, **kwargs)
        m = UserExpense.objects.all()
        serializer2 = UserExpenseSerializer(instance=m, many=True)

        return Response(serializer2.data, status=status.HTTP_201_CREATED)


class UserAPIIncome(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserIncomeSerializer

    def get_queryset(self):
        return UserIncome.objects.filter(user=self.request.user)


class UserAPIAmountOfIncome(RetrieveAPIView):
    """ total incomes for N days """
    permission_classes = [IsAuthenticated]
    serializer_class = UserTotalIncomeSerializer

    def get_object(self):
        return self.request.user


class UserIncomeListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserIncomeSerializer
    queryset = UserIncome.objects.all()






