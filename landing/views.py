import itertools
import json
import random

from django.db.models import Count, Q
from django.http import JsonResponse, Http404, HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from . import helper
from .models import Category, Product, CartItem, Order, Cashier, Faq, PaymentMethod, Cart, NewsLetter
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer, CashierSerializer, FaqSerializer,
    PaymentMethodSerializer, OrderListSerializer, NewsletterSerializer)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_serializer(self, *args, **kwargs):
        return CategorySerializer(self.get_queryset(), context={"request": self.request},
                                  remove_fields=['products'], many=True)

    def get_queryset(self):
        categories = Category.objects.all()
        for category in categories:
            if not len(category.products.all()):
                categories = categories.exclude(id=category.id)
        return categories


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
        query = self.request.query_params.get('q', '')
        categories = self.request.query_params.getlist('categories', [])
        if len(categories):
            return Product.objects.filter(category__in=categories, name__icontains=query)
        return Product.objects.filter(name__icontains=query)


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
        cart = Cart.objects.get(user=self.request.user.id, is_ordered=False)
        request.data['cart'] = cart.id
        # request.data['cart_items'] = json.dumps(get_user_cart(self.request.user.id, self.get_serializer_context()))
        return super(MakeOrder, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class GetOrders(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user)


class SearchOrder(generics.ListAPIView):
    def get_queryset(self):
        transaction = Order.objects.filter(order_id=self.request.query_params.get('orderId', ''))
        if not transaction.exists():
            raise Http404()
        else:
            return transaction[0]

    def get_serializer(self, *args, **kwargs):
        return OrderSerializer(self.get_queryset())


class GetCategory(generics.RetrieveAPIView):
    def get_queryset(self):
        return Category.objects.filter(pk=self.kwargs.get("pk"))

    def get_serializer(self, *args, **kwargs):
        return CategorySerializer(self.get_queryset().first(), remove_fields=["parentCategory"],
                                  context={"request": self.request})


class GetCart(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def list(self, request, *args, **kwargs):
        return Response(helper.get_user_cart(self.request.user.id, self.get_serializer_context()))


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body.decode('utf-8'))
        cart, created = Cart.objects.get_or_create(user_id=user.id, is_ordered=False)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=data['product'],
                                                            measurement_unit_id=data['measurementUnit'],
                                                            defaults={'quantity': data['quantity']})
        if not created:
            cart_item.quantity = cart_item.quantity + data['quantity']
            cart_item.save()
        user_cart = CartItem.objects.filter(cart=cart)
        serializer = CartSerializer(user_cart, context={'request': request}, many=True)
        data = {}
        for product_id, cart_item in itertools.groupby(serializer.data, lambda product: product.get('product').get('id')):
            data[product_id] = list(cart_item)
        return Response({'msg': 'Successfully added to cart', 'cart': data})


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def update_cart(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body.decode('utf-8'))
        quantity = data['quantity']
        product = data['product']
        cart = Cart.objects.get(user=user, is_ordered=False)
        cart_item = CartItem.objects.get(product_id=product, cart=cart)
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
    qs = CartItem.objects.filter(cart__user_id=request.user.id, product_id=data['product'])
    qs.delete()

    return JsonResponse({'msg': 'Successfully deleted from cart'})


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def upload_screenshot(request):
    print(request.POST)
    order_id = request.POST.get('order', None)
    file = request.FILES.get('image', None)
    if not order_id:
        return HttpResponse('Order Id is required', status=400)
    if file and file.size / 1000 > 200:
        return HttpResponse('File required and size must not exceed 200KB', status=400)
    try:
        order1 = Order.objects.get(id=order_id)
        order1.payment_screenshot = file
        order1.save()
    except Order.DoesNotExist:
        return HttpResponse('Order doesn\'t exist', status=404)
    return JsonResponse({'msg': 'Payment Screenshot Uploaded Successfully'})


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def order(request):
    data = json.loads(request.body.decode('utf-8'))


class FaqsView(generics.ListAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()
    pagination_class = None


class PaymentMethodsView(generics.ListAPIView):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.filter(active=True)


class NewsLetterSubscribe(generics.ListCreateAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsletterSerializer
