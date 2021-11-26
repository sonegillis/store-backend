import itertools
import json
import random

from django.db.models import Count
from django.http import JsonResponse, Http404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Category, Product, CartItem, Order, Cashier
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer, CashierSerializer


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_serializer(self, *args, **kwargs):
        return CategorySerializer(self.get_queryset(), context={"request": self.request},
                                  remove_fields=['products'], many=True)

    def get_queryset(self):
        return Category.objects.all()


class CreateCategory(generics.CreateAPIView):
    # serializer_class = CategorySerializer(remove_fields=['products'])

    def get_serializer(self, *args, **kwargs):
        return CategorySerializer(remove_fields=['products'], data=self.request.data)


class CreateProduct(generics.CreateAPIView):

    def get_serializer(self, *args, **kwargs):
        print(self.request.FILES)
        return ProductSerializer(data=self.request.data)


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
    pagination_class = None

    def get_queryset(self):
        qs = Category.objects.annotate(cnt=Count('products')).order_by('-cnt')
        return Category.objects.filter(pk__in=qs[:2])


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product
    serializer_class = ProductSerializer


class AvailableCashiers(generics.ListAPIView):
    serializer_class = CashierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cashier.objects.filter(is_available=True)

    def get_serializer(self, *args, **kwargs):
        return CashierSerializer(random.choice(self.get_queryset()))


class MakeOrder(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        return super(MakeOrder, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class SearchOrder(generics.ListAPIView):

    def get_queryset(self):
        transaction = Order.objects.filter(order_id=self.request.query_params.get('orderId', ''))
        if not transaction.exists():
            raise Http404()
        else:
            return transaction[0]

    def get_serializer(self, *args, **kwargs):
        return OrderSerializer(self.get_queryset())


class GetCart(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user_id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        cart = self.get_serializer(self.get_queryset(), many=True)
        data = {}
        for product_id, cart_item in itertools.groupby(cart.data, lambda product: product.get('product').get('id')):
            data[product_id] = list(cart_item)
        return Response(data)


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body.decode('utf-8'))
        cart_item, created = CartItem.objects.get_or_create(user_id=user.id, product_id=data['product'],
                                                            measurement_unit_id=data['measurementUnit'],
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


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def order(request):
    data = json.loads(request.body.decode('utf-8'))
