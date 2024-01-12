from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from accounts.views import UsersAPIList, UserAPIView
from accounts.views import UserAPICatigories, UserAPIAddCatigories
from accounts.views import UserAPIAddExpense, UserAPIAddIncome, UserAPIExpense, UserAPIIncome, UserAPIAmountOfExpense, UserAPIAmountOfIncome

from categories.views import CategoryAPIList, CategoryAPIView, CategoryAPIDelete, CategoryAPIUpdate

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from djoser import views

schema_view = get_schema_view(
       openapi.Info(
           title="API for authorization users",
           default_version='v1',
           description="API return 2 fields 'username' and 'password'. They get 30 and 255 symbols",
           terms_of_service="---",
           contact=openapi.Contact(email="test@test.com"),
           license=openapi.License(name="Open API and you can use it anywhere, if you found it"),
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
    )


urlpatterns = [
    path("admin/", admin.site.urls),

    # юзеры
    path("api/v1/users/", UsersAPIList.as_view(), name="users-list"),
    path("api/v1/user/<int:pk>", UserAPIView.as_view(), name="user-view"),

    path("api/v1/user/<int:pk>/categories", UserAPICatigories.as_view(), name="user-categories-list"),
    path("api/v1/user/add_categories", UserAPIAddCatigories.as_view(), name="user-add-categories-list"),

    path("api/v1/user/<int:pk>/expense", UserAPIExpense.as_view(), name="user-expense-list"),
    path("api/v1/user/<int:pk>/amount_of_expense/<int:days>", UserAPIAmountOfExpense.as_view(), name="user-amout-of-expense"),
    path("api/v1/user/add_expense", UserAPIAddExpense.as_view(), name="user-add-expense"),

    path("api/v1/user/<int:pk>/income", UserAPIIncome.as_view(), name="user-income-list"),
    path("api/v1/user/<int:pk>/amount_of_income/<int:days>", UserAPIAmountOfIncome.as_view(), name="user-amout-of-income"),
    path("api/v1/user/add_income", UserAPIAddIncome.as_view(), name="user-add-income"),

    # категории
    path("api/v1/category/", CategoryAPIList.as_view(), name="categories-list"),
    path("api/v1/category/<int:pk>", CategoryAPIView.as_view(), name="category-view"),
    path("api/v1/category/delete/<int:pk>", CategoryAPIDelete.as_view(), name="category-delete"),
    path("api/v1/category/update/<int:pk>", CategoryAPIUpdate.as_view(), name="category-update"),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

    # path('api/v1/auth/user/', views.UserViewSet.as_view({'post': 'activation'})),
    path("api/v1/auth/", include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
