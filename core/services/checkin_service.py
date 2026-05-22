from django.db.models import Prefetch
from checkins.models import CheckIn
from customers.models import Subscription
from .subscription_service import SubscriptionService


class CheckInService:
    """Service for handling check-in business logic"""

    @staticmethod
    def get_optimized_checkin_queryset():
        """
        Returns optimized queryset with all related data
        Use this in your ViewSet to avoid N+1 queries
        """
        # Get subscription annotations
        subscription_annotations = SubscriptionService.get_latest_subscription_annotation()

        return CheckIn.objects.select_related(
            'customer',
            'created_by'
        ).annotate(**subscription_annotations)

    @staticmethod
    def get_checkin_with_subscription(checkin_obj):
        """
        Enrich a check-in object with formatted subscription data
        """
        subscription_data = {
            'kind': getattr(checkin_obj, 'latest_sub_kind', None),
            'start_date': getattr(checkin_obj, 'latest_sub_start_date', None),
            'end_date': getattr(checkin_obj, 'latest_sub_end_date', None),
            'session_limit': getattr(checkin_obj, 'latest_sub_session_limit', None),
            'sessions_used': getattr(checkin_obj, 'latest_sub_sessions_used', None),
        }

        return SubscriptionService.format_subscription_data(subscription_data)
