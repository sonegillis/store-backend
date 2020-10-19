from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CartItem, Order


@receiver([post_save], sender=Order)
def delete_user_cart(sender, instance, created, **kwargs):
    if created:
        CartItem.objects.filter(user_id=instance.user.id).delete()

