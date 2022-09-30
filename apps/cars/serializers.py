import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator

from apps.cars.models import Color, Model, Brand, Order


class CarColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'code_name', 'hex_value')
        read_only_fields = ('id',)

    def validate(self, attrs):
        if not re.findall(r'^#(?:[0-9a-fA-F]{3}){1,2}$', attrs.get('hex_value', '')):
            raise ValidationError('Некорректный код цвета', 'hex_color_error')

        if not re.findall(r'[A-Za-z\d\_]+', attrs.get('code_name', '')):
            raise ValidationError('Некорректное кодовое название', 'color_cn_error')

        return attrs


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'code_name')
        read_only_fields = ('id',)


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'code_name')
        read_only_fields = ('id',)


class CarOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    color = CarColorSerializer(default=None, read_only=True)
    model = CarModelSerializer(default=None, read_only=True)
    brand = CarBrandSerializer(default=None, read_only=True)

    color_id = serializers.IntegerField(write_only=True, allow_null=True)
    model_id = serializers.IntegerField(write_only=True, allow_null=True)
    brand_id = serializers.IntegerField(write_only=True, allow_null=True)

    date = serializers.DateField(required=False, allow_null=True)
    amount = serializers.IntegerField(validators=[MinValueValidator(0, 'Кол-во не может быть отрициательным')])

    class Meta:
        model = Order
        fields = ('id', 'color', 'model', 'brand',
                  'color_id', 'brand_id', 'model_id', 'amount', 'date')
