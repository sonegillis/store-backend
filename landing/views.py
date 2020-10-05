import json

from django.db.models import Count
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Category, Product, CartItem
from .serializers import CategorySerializer, ProductSerializer, CartSerializer


class CategoryView(generics.ListAPIView):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.all()


class ProductView(generics.ListAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        categories = self.request.query_params.getlist('categories', [])
        if len(categories):
            return Product.objects.filter(category__in=categories)
        return Product.objects.all()


class MainCategoriesView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Category.objects.values('id', 'products').annotate(total=Count('products')) \
                 .order_by('-total').values_list('id', flat=True)[:2]
        return Category.objects.filter(pk__in=qs)


class GetCart(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user_id=self.request.user.id)


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body.decode('utf-8'))
        cart_item, created = CartItem.objects.get_or_create(user_id=user.id, product_id=data['product'],
                                                            defaults={'quantity': data['quantity']})
        if not created:
            cart_item.quantity = cart_item.quantity + data['quantity']
            cart_item.save()
        user_cart = CartItem.objects.filter(user_id=user.id)
        serializer = CartSerializer(user_cart, context={'request': request}, many=True)
        return Response({'msg': 'Successfully added to cart', 'cart': serializer.data})


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_cart(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body.decode('utf-8'))
        quantity = data['quantity']
        product = data['product']
        cart_item = CartItem.objects.get(product_id=product, user_id=user.id)
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()
            serializer = CartSerializer(CartItem.objects.filter(user_id=user.id),
                                        context={'request': request}, many=True)
            return Response({'msg': 'Successfully updated cart', 'cart': serializer.data})


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_from_cart(request):
    data = json.loads(request.body.decode('utf-8'))
    qs = CartItem.objects.filter(user_id=request.user.id, product_id=data['product'])
    qs.delete()

    return JsonResponse({'msg': 'Successfully deleted from cart'})
