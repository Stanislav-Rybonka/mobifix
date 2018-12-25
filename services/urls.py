from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from services import api as api_views

router = DefaultRouter()

router.register(
    prefix='orders',
    viewset=api_views.OrderModelViewSet,
    base_name='orders',
)
urlpatterns = [
    url(r'^services/', api_views.ServiceListAPIView.as_view(), name='services'),
    url(r'^', include(router.urls)),
]