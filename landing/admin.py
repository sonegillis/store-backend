from django.contrib import admin

# Register your models here.
from .models import Category, Product, MeasurementUnit


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(MeasurementUnit)
class CategoryAdmin(admin.ModelAdmin):
    pass
