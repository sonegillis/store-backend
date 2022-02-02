from django.contrib import admin

# Register your models here.
from .forms import OrderForm
from .models import Category, Product, MeasurementUnit, \
    Cashier, ProductImage, Advert, AdvertProduct, \
    ProductMeasurementUnit, Faq, PaymentMethod, OrderStatus, Order
from .widgets import CartItemWidget


class ProductInline(admin.StackedInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (ProductInline,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("get_image", "get_thumbnail")


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('order_id', )
    readonly_fields = ('order_id', 'cost', 'state', 'city', 'shipping_address', 'phone_number')
    form = OrderForm

    def has_add_permission(self, request):
        return False


@admin.register(Cashier)
class CashierAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('product',)
    fields = ('product', 'image', 'image_tag')
    readonly_fields = ('image_tag',)


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    fields = ('question', 'answer', 'ordering')


@admin.register(PaymentMethod)
class PaymentMethodsAdmin(admin.ModelAdmin):
    readonly_fields = ('get_logo',)


@admin.register(OrderStatus)
class OrderStatus(admin.ModelAdmin):
    pass
