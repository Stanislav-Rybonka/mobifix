from django.utils.crypto import get_random_string
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from services.models import Order
from services.models import Service
from services.serializers import OrderModelSerializer
from services.serializers import ServiceModelSerializer
from services.serializers import OrderConfirmModelSerializer


class ServiceListAPIView(ListAPIView):
    serializer_class = ServiceModelSerializer
    queryset = Service.objects.all()


class OrderModelViewSet(ModelViewSet):
    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            number=get_random_string(5).upper(),
        )

    def perform_update(self, serializer):
        serializer.save(
            user=self.request.user,
        )

    def get_serializer_class(self):
        if self.action == 'confirm_order':
            return OrderConfirmModelSerializer
        return self.serializer_class

    @action(detail=True, methods=['patch'])
    def confirm_order(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        received_verification_code = serializer.validated_data.get('verification_code')
        status = serializer.validated_data.get('status')
        actual_verification_code = order.phone_verification_code
        if received_verification_code == actual_verification_code:
            order.is_phone_verified = True
            order.status = status
            order.save(update_fields=['is_phone_verified', 'status'])
            order.user.send_sms(
                body='Your Order track number: [{}]'.format(
                    order.number
                ),
                sms_to=order.customer_phone,
            )
        return Response(OrderModelSerializer(instance=order).data)
