import string
import random

from django.db import models
# Create your models here.
from django.db.models.signals import post_save


class Category(models.Model):
    name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    short_description = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parentCategory = models.ForeignKey('self', on_delete=models.CASCADE,
                                       null=True, blank=True, related_name='categories')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class MeasurementUnit(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'MeasurementUnits'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='products')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.DO_NOTHING)
    in_stock = models.BooleanField(default=True)
    price_per_unit = models.FloatField()
    image = models.ImageField(upload_to='product_images')
    rating = models.FloatField(default=5)
    min_order = models.FloatField()
    discount_price_per_unit = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('user', 'product',)

    def __str__(self):
        return "{} has ordered {} of {}".format(self.user.email, self.quantity, self.product.name)


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=30, unique=True)
    cart_items = models.JSONField('items ordered')
    cost = models.FloatField()
    payment_method = models.CharField(max_length=30, default='')
    shipping_address = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=15, default='')

    @staticmethod
    def get_random_string():
        lower_case_letters = string.ascii_lowercase
        upper_case_letters = string.ascii_uppercase
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return ''\
            .join(random.choice(random.choice([lower_case_letters, upper_case_letters, numbers])) for i in range(6))

    def __str__(self):
        return self.order_id

    def save(self, **kwargs):
        self.order_id = 'MEDICANN-'+self.get_random_string()
        super(Order, self).save(**kwargs)
        

class Cashier(models.Model):
    name = models.CharField(max_length=100, verbose_name    ='Name of cashier')
    phone_number = models.CharField(max_length=15, verbose_name='Phone number of cahsier')
    is_available = models.BooleanField(default=True, verbose_name='Only cashiers available will be located by clients')

    def __str__(self):
        return self.name
