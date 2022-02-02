import itertools

from landing.models import Cart, CartItem
from landing.serializers import CartSerializer


def get_user_cart(user_id, context):
    cart, _ = Cart.objects.get_or_create(user_id=user_id, is_ordered=False)
    return get_user_cart_from_cart(cart, context)


def get_user_cart_from_cart(cart, context):
    items = CartSerializer(CartItem.objects.filter(cart=cart), many=True, context=context)
    data = {}
    for product_id, cart_item in itertools.groupby(items.data, lambda product: product.get('product').get('id')):
        data[product_id] = list(cart_item)
    return data
