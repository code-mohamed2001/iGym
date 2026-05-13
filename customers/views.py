from django.db.models.deletion import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.service import create_subscription_with_invoice

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

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        blocked_by = []
        if customer.checkins.exists():
            blocked_by.append("checkins")
        if customer.invoices.exists():
            blocked_by.append("invoices")
        if blocked_by:
            parts = []
            if "checkins" in blocked_by:
                parts.append("check-in records")
            if "invoices" in blocked_by:
                parts.append("invoice records")
            if len(parts) == 2:
                detail = (
                    "This customer cannot be deleted while they have "
                    "check-in and invoice records."
                )
            else:
                detail = (
                    f"This customer cannot be deleted while they have {parts[0]}."
                )
            return Response(
                {
                    "code": "customer_delete_blocked",
                    "detail": detail,
                    "blocked_by": blocked_by,
                },
                status=status.HTTP_409_CONFLICT,
            )
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    "code": "customer_delete_blocked",
                    "detail": (
                        "This customer cannot be deleted because related "
                        "records still exist."
                    ),
                },
                status=status.HTTP_409_CONFLICT,
            )


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.select_related(
        'created_by', 'customer').all()
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        subscription = create_subscription_with_invoice(
            created_by=request.user,
            customer=data["customer"],
            kind=data["kind"],
            price=data["price"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            session_limit=data.get("session_limit"),
            sessions_used=data.get("sessions_used", 0),
        )
        output = self.get_serializer(subscription)
        headers = self.get_success_headers(output.data)
        return Response(
            output.data, status=status.HTTP_201_CREATED, headers=headers
        )

