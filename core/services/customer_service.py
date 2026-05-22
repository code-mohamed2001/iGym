# core/services/customer_service.py
from datetime import date

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone


class CustomerService:
    """Service to handle customer-related operations across apps"""

    @staticmethod
    def get_customer_model():
        """Dynamically get Customer model"""
        return apps.get_model('customers', 'Customer')

    @staticmethod
    def get_subscription_model():
        """Dynamically get Subscription model"""
        return apps.get_model('customers', 'Subscription')

    @staticmethod
    def get_customer_by_barcode(barcode):
        """Get customer by barcode"""
        Customer = CustomerService.get_customer_model()
        try:
            return Customer.objects.get(barcode=barcode)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def customer_exists(barcode):
        """Check if customer exists"""
        Customer = CustomerService.get_customer_model()
        return Customer.objects.filter(barcode=barcode).exists()

    @staticmethod
    def get_latest_subscription(customer):
        """Get the latest subscription (could be expired)"""
        Subscription = CustomerService.get_subscription_model()
        return Subscription.objects.filter(customer=customer).order_by('-created_at').first()

    @staticmethod
    def get_active_subscription(customer):
        """Get only active (non-expired) subscriptions"""
        Subscription = CustomerService.get_subscription_model()
        today = timezone.now().date()

        return Subscription.objects.filter(
            customer=customer
        ).order_by('-created_at').first()

    @staticmethod
    @transaction.atomic
    def process_checkin_session(customer, visit_type):
        """
        Process check-in and increment session usage if applicable

        Args:
            customer: Customer instance
            visit_type: Type of visit (subscription, walk_in, etc.)

        Returns:
            dict: Result with subscription info and status
        """
        result = {
            'success': True,
            'subscription_used': False,
            'message': None,
            'subscription': None
        }

        # Only process session packs for subscription visits
        if visit_type == 'subscription':
            latest_sub = CustomerService.get_active_subscription(customer)
            # print(latest_sub.end_date)

            if not latest_sub:
                result['success'] = False
                result['message'] = 'No active subscription found'
                return result

            today = date.today()
            print(today)
            if latest_sub.end_date < today:
                result['success'] = False
                result['message'] = f'Subscription expired on {latest_sub.end_date}'
                return result

            if latest_sub and latest_sub.kind == 'session_pack':
                # Check if subscription is still valid
                today = timezone.now().date()

                if latest_sub.end_date and latest_sub.end_date < today:
                    result['success'] = False
                    result['message'] = 'Session pack has expired'
                    return result

                # Check if there are remaining sessions
                if latest_sub.session_limit is not None:
                    remaining = latest_sub.session_limit - latest_sub.sessions_used

                    if remaining <= 0:
                        result['success'] = False
                        result['message'] = 'No remaining sessions in this pack'
                        return result

                # Increment sessions_used
                latest_sub.sessions_used += 1
                latest_sub.save(update_fields=['sessions_used'])

                result['subscription_used'] = True
                result['message'] = f'Session used. {latest_sub.session_limit - latest_sub.sessions_used} sessions remaining'
                result['subscription'] = {
                    'kind': latest_sub.kind,
                    'remaining_sessions': latest_sub.session_limit - latest_sub.sessions_used,
                    'total_sessions': latest_sub.session_limit,
                    'used_sessions': latest_sub.sessions_used,
                }

        return result
