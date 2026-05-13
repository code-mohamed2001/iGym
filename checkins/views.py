from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from customers.models import Customer, Subscription

from .models import CheckIn
from .serializers import CheckInSerializer


class CheckInViewSet(ModelViewSet):
    queryset = CheckIn.objects.select_related("customer", "created_by").all()
    serializer_class = CheckInSerializer

    def perform_create(self, serializer):
        customer_barcode = serializer.validated_data.get("customer_barcode")
        today = timezone.now().date()

        customer = get_object_or_404(Customer, barcode=customer_barcode)

        with transaction.atomic():
            latest_sub = (
                Subscription.objects.select_for_update()
                .filter(customer=customer)
                .order_by("-created_at")
                .first()
            )

            if latest_sub is None:
                raise ValidationError(
                    {"detail": "No subscription found for this customer."})

            is_expired = (
                latest_sub.status != "active"
                or latest_sub.end_date < today
                or (
                    latest_sub.kind == "session_pack"
                    and latest_sub.session_limit is not None
                    and latest_sub.sessions_used >= latest_sub.session_limit
                )
            )

            if latest_sub.kind == "session_pack":
                if (
                    latest_sub.session_limit is not None
                    and latest_sub.sessions_used + 1 > latest_sub.session_limit
                ):
                    raise ValidationError(
                        {"detail": "No sessions remaining in this pack."}
                    )

            if is_expired:
                raise ValidationError({"detail": "Subscription is expired."})

            serializer.save(
                created_by=self.request.user,
                customer=customer,
                customer_barcode=customer_barcode,
            )

            if latest_sub.kind == "session_pack":
                Subscription.objects.filter(pk=latest_sub.pk).update(
                    sessions_used=F("sessions_used") + 1
                )
