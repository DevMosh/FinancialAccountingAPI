from django.urls import path
from . import views

urlpatterns = [
    path("category/<int:pk>/", views.CategoryAPI.as_view(), name="category-api"),  # get, put, path, delete
    path("category/", views.CreateCategoryAPI.as_view(), name="category-create-api")  # post
]