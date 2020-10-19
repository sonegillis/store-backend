from django.contrib import admin
from django.urls import path

from .views import (
    CategoryView, ProductView, MainCategoriesView,
    add_to_cart, delete_from_cart, GetCart, update_cart,
    MakeOrder, AvailableCashiers, SearchOrder)


urlpatterns = [
    path('categories', CategoryView.as_view()),
    path('products', ProductView.as_view()),
    path('main-categories', MainCategoriesView.as_view()),
    path('category/<int:pk>/products', ProductView.as_view()),
    path('add-to-cart', add_to_cart),
    path('get-cart', GetCart.as_view()),
    path('delete-from-cart', delete_from_cart),
    path('update-cart', update_cart),
    path('make-order', MakeOrder.as_view()),
    path('cashiers', AvailableCashiers.as_view()),
    path('search-order', SearchOrder.as_view())
]
