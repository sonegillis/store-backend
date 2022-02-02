from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CartItem, Order, Cart


@receiver([post_save], sender=Order)
def delete_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.filter(id=instance.cart.id).update(is_ordered=True)

