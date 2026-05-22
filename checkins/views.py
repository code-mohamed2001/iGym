from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from customers.models import Customer, Subscription

from .models import CheckIn
from .serializers import CheckInSerializer
from core.services.checkin_service import CheckInService


class CheckInViewSet(ModelViewSet):
    serializer_class = CheckInSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        'customer': ['exact'],
        'visit_type': ['exact'],
        'created_at': ['date', 'gte', 'lte'],
    }

    def get_queryset(self):
        """Use service layer to get optimized queryset"""
        return CheckInService.get_optimized_checkin_queryset()
    
    def perform_create(self, serializer):
        """
        Save the check-in with the current user as created_by
        """
        serializer.save(created_by=self.request.user)
