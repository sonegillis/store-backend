import json

from django.forms import widgets
from django.template import loader, Context
from django.utils.safestring import mark_safe

from landing import helper
from landing.models import Product, CartItem, Cart


class CartItemWidget(widgets.Textarea):
    template_name = 'landing/cart-item.html'
    request = None
    class Media:
        css = {
            'all': ('css/bootstrap.min.css', 'css/styles.css')
        }

    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}
        self.request = kwargs['request'] if 'request' in kwargs else None
        super().__init__(attrs)

    def render(self, name, value, attrs=None, **kwargs):
        cart = Cart.objects.get(id=value)
        context = self.get_context(name, value, attrs)
        context['request'] = self.request
        cart_items = dict(helper.get_user_cart(user_id=cart.user.id, context=context))
        template = loader.get_template(self.template_name).render({'cartItems': cart_items, 'cart': cart.id})
        return mark_safe(template)
