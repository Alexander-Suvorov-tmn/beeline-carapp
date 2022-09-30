from django.urls import path
from rest_framework.routers import SimpleRouter
from apps.cars import views


router = SimpleRouter()
router.register('api/colors', views.CarColorViewSet)
router.register('api/models', views.CarModelViewSet)
router.register('api/brands', views.CarBrandViewSet)
router.register('api/orders', views.CarOrderViewSet)

urlpatterns = [path('api/orders-count/', views.CarAttributesCountAPIView.as_view()), *router.urls]
