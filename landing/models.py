import string
import random

from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.utils import timezone

from jsonfield import JSONField


class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(null=True)
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
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='products')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images')
    rating = models.FloatField(default=5)
    visible = models.BooleanField(default=True, help_text="Appear in product listings")
    description = models.TextField(null=True)
    thumbnail = models.ImageField(null=True)

    class Meta:
        verbose_name_plural = 'Products'

    def get_image(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="/media/%s" width="150" height="150"/>' % self.image.name)

    def get_thumbnail(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="/media/%s" width="150" height="150"/>' % self.thumbnail.name)

    get_image.short_description = "Image Preview"
    get_thumbnail.short_description = "Thumbnail Preview"

    def __str__(self):
        return self.name


class ProductMeasurementUnit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='measurement_units')
    measurement_unit = models.ForeignKey('MeasurementUnit', on_delete=models.CASCADE, related_name='unit')
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    min_order = models.IntegerField(default=1)

    class Meta:
        unique_together = ['product', 'measurement_unit']

    def __str__(self):
        return f"{self.product.name}_{self.measurement_unit.name}_${self.price}"


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='cart')
    date_created = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)


class CartItem(models.Model):
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='carts')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items', null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='products')
    measurement_unit = models.ForeignKey('MeasurementUnit', on_delete=models.CASCADE, related_name='measurement_units')
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('cart', 'product', 'measurement_unit')

    def __str__(self):
        return "{} has ordered {} of {}".format(self.cart.user.email, self.quantity, self.product.name)


class Order(models.Model):
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE, null=True, unique=True)
    order_id = models.CharField(max_length=30, unique=True)
    cost = models.FloatField()
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, default='1')
    state = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    shipping_address = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=15, default='')
    is_paid = models.BooleanField(default=False)
    order_status = models.ForeignKey('OrderStatus', null=True, on_delete=models.SET_NULL, related_name='orders')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    payment_screenshot = models.ImageField(null=True, upload_to='payment_screenshots')

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
        if not self.order_id:
            self.order_id = 'DCGASOVERFLOW-' + self.get_random_string()
        super(Order, self).save(**kwargs)
        

class Cashier(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name of cashier')
    phone_number = models.CharField(max_length=15, verbose_name='Phone number of cashier')
    email = models.CharField(max_length=50)
    signature = models.ImageField(upload_to='signatures/', null=True)
    is_available = models.BooleanField(default=True, verbose_name='Only cashiers available will be located by clients')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % self.image.name)

    image_tag.short_description = 'Image Preview'
    image_tag.allow_tags = True

    def __str__(self):
        return self.product.name + "_" + self.image.name


class Advert(models.Model):
    image = models.ImageField(),
    name = models.CharField(max_length=50),
    add_to_cart = models.BooleanField()
    price = models.FloatField(null=True)

    def __str__(self):
        return self.name


class AdvertProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    ordering = models.IntegerField(default=0)

    def __str__(self):
        return "{}: {} => {}".format(self.ordering, self.question, self.answer)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=50)
    description = models.TextField()
    logo = models.ImageField()
    detail = models.CharField(max_length=50, blank=True)
    detail_name = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=False)
    show_qrcode = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_logo(self):
        from django.utils.html import mark_safe
        return mark_safe('<img src="/media/%s" width="150" height="150"/>' % self.logo.name)


class OrderStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Order Status'

    def __str__(self):
        return self.name


class NewsLetter(models.Model):
    email = models.EmailField(max_length=50, unique=True)

    def __str__(self):
        return self.email
