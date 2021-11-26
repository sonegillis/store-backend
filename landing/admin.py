from django.contrib import admin

# Register your models here.
from .models import Category, Product, MeasurementUnit, \
    Cashier, ProductImage, Advert, AdvertProduct, \
    ProductMeasurementUnit


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("get_image",)


class ProductStackedInline(admin.StackedInline):
    model = Product


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    pass


class MeasurementUnitStackedInline(admin.StackedInline):
    model = MeasurementUnit


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductMeasurementUnit)
class ProductMeasurementUnitAdmin(admin.ModelAdmin):
    raw_id_fields = ('product',)


@admin.register(AdvertProduct)
class AdvertProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Cashier)
class CashierAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('product',)
    fields = ('product', 'image', 'image_tag')
    readonly_fields = ('image_tag',)
