from django.db import models
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    short_description = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    parentCategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

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
