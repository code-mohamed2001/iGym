# checkins/views.py
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CheckIn
from .serializers import CheckInSerializer
from .services import CheckInService


class CheckInViewSet(ModelViewSet):
    serializer_class = CheckInSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        'visit_type': ['exact'],
        'created_at': ['date', 'gte', 'lte'],
    }

    def get_queryset(self):
        return CheckIn.objects.select_related(
            'customer',
            'created_by'
        ).prefetch_related(
            'customer__subscriptions'  # ✅ prefetch to avoid N+1 on list
        ).all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        # 1. validate input shape only
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        barcode = serializer.validated_data['barcode']
        visit_type = serializer.validated_data.get(
            'visit_type', 'subscription')

        # 2. all business logic lives here
        try:
            result = CheckInService.process_checkin(
                barcode=barcode,
                visit_type=visit_type,
                created_by=request.user,
            )
        except ValidationError as e:
            return Response(
                {"error": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. build response directly from the clean dataclass
        return Response({
            "checkin_id": result.checkin_id,
            "customer_barcode": result.customer_barcode,
            "customer_name": result.customer_name,
            "visit_type": result.visit_type,
            "subscription_kind": result.subscription_kind,
            'session_limit': result.session_limit,
            'sessions_used': result.sessions_used,  # ✅ new
            "sessions_remaining": result.sessions_remaining,
            "subscription_start_date": result.subscription_start_date,  # ✅ new
            "subscription_end_date": result.subscription_end_date,      # ✅ new
            "checked_in_at": result.checked_in_at,
        }, status=status.HTTP_201_CREATED)
