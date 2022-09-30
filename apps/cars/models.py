from django.db import models
from django.utils import timezone


class Color(models.Model):
    """ Цвет автомобилей """

    class Meta:
        db_table = 'colors'
        verbose_name = 'Цвета'

    code_name = models.CharField('Кодовое наименование цвета', default='white', max_length=15)
    hex_value = models.CharField('HEX-значение цвета #AABBCC', default='#ffffff', max_length=7)


class Brand(models.Model):
    """ Марка автомобиля """

    class Meta:
        db_table = 'brands'
        verbose_name = 'Марки авто'

    code_name = models.CharField('Кодовое наименование марки автомобиля', max_length=125)


class Model(models.Model):
    """ Модели автомобилей """

    class Meta:
        db_table = 'models'
        verbose_name = 'Модели авто'

    code_name = models.CharField('Кодовое наименование модели автомобиля', max_length=125)


class Order(models.Model):
    """ Заказы """

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказы'

    color = models.ForeignKey('cars.Color', on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey('cars.Brand', on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey('cars.Model', on_delete=models.SET_NULL, null=True)
    date = models.DateField('Дата заказа', default=timezone.now().date())
    amount = models.PositiveIntegerField('Кол-во', default=0)
