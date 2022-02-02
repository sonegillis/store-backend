import json

from django import template

register = template.Library()


def get_dict_item_from_key(obj, key):
    print('object is ', obj)
    print('key is ', key)
    print('value is ', obj.get(key))
    return obj[key]


def get_cart_subtotal(orders):
    total = 0
    for order in orders:
        total += order['quantity'] * (order['discount_price'] if order['discount_price'] else order['price'])
    return total


def get_order_total(cart_items):
    total = 0
    for product_id, orders in cart_items.items():
        total += get_cart_subtotal(orders)
    return total


def json_dumps(json_obj):
    return json.dumps(json_obj)


register.filter('get_dict_item_from_key', get_dict_item_from_key)
register.filter('get_cart_subtotal', get_cart_subtotal)
register.filter('get_order_total', get_order_total)
register.filter('json_dumps', json_dumps)

