from rest_framework.viewsets import ModelViewSet

from .models import Customer, Subscription
from .serializers import (
    CustomerDetailSerializer,
    CustomerSerializer,
    SubscriptionSerializer,
)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related('created_by').all()
    serializer_class = CustomerSerializer
    lookup_field = "barcode"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CustomerDetailSerializer
        return super().get_serializer_class()


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.select_related(
        'created_by','customer').all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
