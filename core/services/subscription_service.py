from django.db.models import Subquery, OuterRef
from customers.models import Subscription  # Adjust import


class SubscriptionService:
    """Service for handling subscription-related business logic"""

    @staticmethod
    def get_latest_subscription_annotation():
        """
        Returns a Subquery annotation for the latest subscription per customer
        Use this in your queryset to avoid N+1 queries
        """
        latest_sub = Subscription.objects.filter(
            customer=OuterRef('customer')
        ).order_by('-created_at')

        return {
            'latest_sub_kind': Subquery(latest_sub.values('kind')[:1]),
            'latest_sub_start_date': Subquery(latest_sub.values('start_date')[:1]),
            'latest_sub_end_date': Subquery(latest_sub.values('end_date')[:1]),
            'latest_sub_session_limit': Subquery(latest_sub.values('session_limit')[:1]),
            'latest_sub_sessions_used': Subquery(latest_sub.values('sessions_used')[:1]),
        }

    @staticmethod
    def format_subscription_data(subscription_data):
        """
        Format subscription data for API response
        Handles different subscription types (monthly, session_pack, etc.)
        """
        if not subscription_data or not subscription_data.get('kind'):
            return None

        result = {
            "kind": subscription_data['kind'],
            "start_date": subscription_data['start_date'],
            "end_date": subscription_data['end_date'],
        }

        if subscription_data['kind'] == "session_pack":
            session_limit = subscription_data.get('session_limit')
            sessions_used = subscription_data.get('sessions_used', 0)
            if session_limit is not None:
                result["remaining_sessions"] = max(
                    0, session_limit - sessions_used)

        return result

    @staticmethod
    def get_latest_subscription_for_customer(customer_id):
        """
        Get the latest subscription for a specific customer
        Use this when you need subscription for a single customer
        """
        try:
            return Subscription.objects.filter(
                customer_id=customer_id
            ).order_by('-created_at').first()
        except Subscription.DoesNotExist:
            return None
