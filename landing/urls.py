from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import (
    CategoryView, ProductView, MainCategoriesView,
    add_to_cart, delete_from_cart, GetCart, update_cart,
    MakeOrder, AvailableCashiers, SearchOrder, CreateCategory, CreateProduct, ProductDetailView,
    GetCategory, FaqsView, PaymentMethodsView, GetOrders, upload_screenshot, NewsLetterSubscribe)


urlpatterns = [
    path('categories', CategoryView.as_view()),
    path('category/<int:pk>', GetCategory.as_view()),
    path('products', ProductView.as_view()),
    path('product-detail/<int:pk>', ProductDetailView.as_view()),
    path('main-categories', MainCategoriesView.as_view()),
    path('category/<int:pk>/products', ProductView.as_view()),
    path('add-to-cart', add_to_cart),
    path('get-cart', GetCart.as_view()),
    path('delete-from-cart', delete_from_cart),
    path('update-cart', update_cart),
    path('make-order', MakeOrder.as_view()),
    path('cashiers', AvailableCashiers.as_view()),
    path('search-order', SearchOrder.as_view()),
    path('create-category', CreateCategory.as_view()),
    path('create-product', CreateProduct.as_view()),
    path('faqs', FaqsView.as_view()),
    path('payment-methods', PaymentMethodsView.as_view()),
    path('orders', GetOrders.as_view()),
    path('newsletter-subscribe', NewsLetterSubscribe.as_view()),
    path('upload-screenshot', upload_screenshot),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
