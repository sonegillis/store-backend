from django.db.models import Sum, Count, Max
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, MainProductSerializer


class CategoryView(generics.ListAPIView):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [permissions.AllowAny]


class ProductView(generics.ListAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        print(self.kwargs)
        return Product.objects.all()


class MainProductsView(generics.ListAPIView):
    serializer_class = MainProductSerializer
    queryset = Product.objects.all()
    # def get_queryset(self):
    #     qs = Product.objects.values('category').annotate(id_count=Count('id'))
    #     qs = qs.filter(id_count=qs.aggregate(Max('id_count'))['id_count__max'])[:2]
    #     for category in qs:
    #         print('category ', category['category'])
    #     # print(Category.objects.all()[0].products.all())
    #     return Category.objects.all()[:2].products.all()
