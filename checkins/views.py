# checkins/views.py
import datetime

import pytz
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from .filters import CheckInFilter
from .models import CheckIn
from .serializers import CheckInSerializer
from .services import CheckInService


class CheckInViewSet(ModelViewSet):
    serializer_class = CheckInSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['customer__barcode']
    filterset_class = CheckInFilter
    permission_classes=[IsAuthenticated,DjangoModelPermissions]

    def get_queryset(self):

        cairo = pytz.timezone('Africa/Cairo')
        today = timezone.localdate()
        start = cairo.localize(
            datetime.datetime.combine(today, datetime.time.min))
        end = cairo.localize(
            datetime.datetime.combine(today, datetime.time.max))
        start_utc = start.astimezone(pytz.utc)
        end_utc = end.astimezone(pytz.utc)

        queryset = CheckIn.objects.select_related(
            'customer',
            'created_by'
        ).prefetch_related(
            'customer__subscriptions'
        ).order_by('-created_at')

        # default to today if no date filter provided
        if 'date' not in self.request.query_params:
            queryset = queryset.filter(created_at__range=(start_utc, end_utc))

        return queryset

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
