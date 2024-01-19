from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from rest_framework_simplejwt import views


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
    path("api/v1/auth/", include('djoser.urls')),
    path('api/v1/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', views.TokenVerifyView.as_view(), name='token_verify'),

    path("admin/", admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

    path('api/v1/', include(('categories.urls', 'categories'), namespace='categories')),
    path('api/v1/', include(('accounts.urls', 'accounts'), namespace='accounts'))
]

# можно еще регистрировать urls через SimpleRouter()

# router = SimpleRouter()
# router.register('users', UsersAPIList.as_view())
