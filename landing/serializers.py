from rest_framework import serializers

from .models import Category, Product, MeasurementUnit


class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    measurement_unit = MeasurementUnitSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MainProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

    def to_representation(self, instance):
        ret = super()
        print('instance ', instance)
