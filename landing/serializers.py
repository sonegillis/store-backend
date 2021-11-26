from rest_framework import serializers

import sys

from .models import Category, Product, MeasurementUnit, CartItem, Order, Cashier, ProductImage, ProductMeasurementUnit


class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

    def to_representation(self, instance):
        data = super(ProductImageSerializer, self).to_representation(instance)
        return self.context.get("request").build_absolute_uri(data.get("image"))


class ProductMeasurementUnitSerializer(serializers.ModelSerializer):
    measurement_unit = MeasurementUnitSerializer()

    class Meta:
        model = ProductMeasurementUnit
        exclude = ("product", )


class ProductSerializer(serializers.ModelSerializer):
    measurement_unit_id = serializers.IntegerField(write_only=True)
    prices = serializers.SerializerMethodField('get_prices')
    images = serializers.SerializerMethodField('get_images')

    class Meta:
        model = Product
        fields = '__all__'

    def get_prices(self, product: Product):
        price = product.measurement_units.all()
        return ProductMeasurementUnitSerializer(price, many=True).data

    def get_images(self, product: Product):
        product_images = product.productimage_set.all()
        return ProductImageSerializer(product_images, context=self.context, many=True).data


class CartProductSerializer(serializers.RelatedField):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'image': self.context['request'].build_absolute_uri(instance.image.url),
        }


class CartSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    measurement_unit = MeasurementUnitSerializer()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['product', 'measurement_unit', 'quantity']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    def __init__(self, *args, **kwargs):
        self.remove_fields = kwargs.pop('remove_fields', None)
        super(CategorySerializer, self).__init__(*args, **kwargs)
        if self.remove_fields:
            for field in self.remove_fields:
                self.fields.pop(field)

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        data = super(CategorySerializer, self).to_representation(instance)
        pk = data.get('id')
        child_categories = CategorySerializer(data=Category.objects.get(id=pk).categories.all(),
                                              remove_fields=self.remove_fields, many=True)
        child_categories.is_valid()
        data['child_categories'] = child_categories.data
        return data


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CashierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashier
        fields = '__all__'
