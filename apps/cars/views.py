from django_filters import filterset
from django.db.models import Count
from rest_framework import viewsets, generics, views
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from apps.cars.models import Color, Brand, Model, Order
from apps.cars.serializers import CarColorSerializer, CarModelSerializer, CarBrandSerializer, CarOrderSerializer


class OrderFilterSet(filterset.FilterSet):
    color = filterset.CharFilter('color__code_name')
    model = filterset.CharFilter('model__code_name')
    brand = filterset.CharFilter('brand__code_name')


class CarColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = CarColorSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = CarModelSerializer


class CarBrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = CarBrandSerializer


class CarOrderViewSet(viewsets.ModelViewSet):
    filterset_class = OrderFilterSet
    serializer_class = CarOrderSerializer
    queryset = Order.objects.select_related('color', 'model', 'brand')


class CarAttributesCountAPIView(views.APIView):

    @silk_profile()
    def get(self, request, *args, **kwargs):
        color = Color.objects.annotate(orders=Count('order')).values('code_name', 'orders')
        model = Model.objects.annotate(orders=Count('order')).values('code_name', 'orders')
        brand = Brand.objects.annotate(orders=Count('order')).values('code_name', 'orders')

        return Response({
            'colors': color,
            'models': model,
            'brands': brand
        })
