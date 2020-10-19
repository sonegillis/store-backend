from rest_framework import serializers

import sys

from .models import Category, Product, MeasurementUnit, CartItem, Order, Cashier


class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    measurement_unit = MeasurementUnitSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        data = super(CategorySerializer, self).to_representation(instance)
        pk = data.get('id')
        child_categories = CategorySerializer(data=Category.objects.get(id=pk).categories.all(), many=True)
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
