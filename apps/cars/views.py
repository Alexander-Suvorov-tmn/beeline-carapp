from django_filters import filterset
from django.db.models import Count
from rest_framework import viewsets, views
from rest_framework.response import Response

from apps.cars.models import Color, Brand, Model, Order
from apps.cars.serializers import CarColorSerializer, CarModelSerializer, CarBrandSerializer, CarOrderSerializer


class OrderFilterSet(filterset.FilterSet):
    color = filterset.CharFilter('color__code_name')
    model = filterset.CharFilter('model__code_name')
    brand = filterset.CharFilter('brand__code_name')


class CarColorViewSet(viewsets.ModelViewSet):
    """ CRUD для работы с цветами авто """
    queryset = Color.objects.all()
    serializer_class = CarColorSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    """ CRUD для работы с моделями авто """
    queryset = Model.objects.all()
    serializer_class = CarModelSerializer


class CarBrandViewSet(viewsets.ModelViewSet):
    """ CRUD для работы с марками авто """
    queryset = Brand.objects.all()
    serializer_class = CarBrandSerializer


class CarOrderViewSet(viewsets.ModelViewSet):
    """ CRUD для работы с заказами """
    filterset_class = OrderFilterSet
    serializer_class = CarOrderSerializer
    queryset = Order.objects.select_related('color', 'model', 'brand')


class CarAttributesCountAPIView(views.APIView):
    """ API для вывода список цветов, моделей и марок """

    def get(self, request, *args, **kwargs):
        color = Color.objects.annotate(orders=Count('order')).values('code_name', 'orders')
        model = Model.objects.annotate(orders=Count('order')).values('code_name', 'orders')
        brand = Brand.objects.annotate(orders=Count('order')).values('code_name', 'orders')

        return Response({
            'colors': color,
            'models': model,
            'brands': brand
        })
