from django.contrib import admin
from django.urls import path

from .views import CategoryView, ProductView, MainProductsView


urlpatterns = [
    path('categories', CategoryView.as_view()),
    path('products', ProductView.as_view()),
    path('main-products', MainProductsView.as_view()),
    path('category/<int:pk>/products', ProductView.as_view()),
]
