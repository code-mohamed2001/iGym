# checkins/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from dataclasses import dataclass
from customers.models import Customer, Subscription


@dataclass
class CheckInResult:
    checkin_id: int
    customer_barcode: str
    customer_name: str
    visit_type: str
    subscription_kind: str | None
    session_limit: int | None
    sessions_used: int | None
    sessions_remaining: int | None
    subscription_start_date: str | None  # ✅ new
    subscription_end_date: str | None    # ✅ new
    checked_in_at: str


class CheckInService:

    @staticmethod
    def _get_active_subscription(customer: Customer) -> Subscription | None:
        """
        Fetch the most recent active subscription for the customer.
        Returns None if no active subscription exists.
        """
        return (
            customer.subscriptions
            .filter(status="active")
            .order_by('-created_at')
            .first()
        )

    @staticmethod
    @transaction.atomic
    def process_checkin(barcode: str, visit_type: str, created_by) -> CheckInResult:
        # 1. fetch customer by barcode
        try:
            customer = Customer.objects.get(barcode=barcode)
        except Customer.DoesNotExist:
            raise ValidationError(
                f"No customer found with barcode '{barcode}'")

        # 2. handle subscription visit type
        subscription = None

        if visit_type == "subscription":
            subscription = CheckInService._get_active_subscription(customer)

            if subscription is None:
                raise ValidationError("Customer has no active subscription")

            if not subscription.is_active():
                raise ValidationError("Customer subscription is expired")

            # 3. consume a session if session pack
            if subscription.kind == "session_pack":
                subscription.sessions_used += 1
                subscription.save()

        # 4. create the checkin record
        # import here to avoid any circular import risk
        from .models import CheckIn
        checkin = CheckIn.objects.create(
            customer=customer,
            visit_type=visit_type,
            created_by=created_by,
        )

        # 5. build and return clean result
        return CheckInResult(
            checkin_id=checkin.id,
            customer_barcode=customer.barcode,
            customer_name=customer.full_name,
            visit_type=visit_type,
            subscription_kind=subscription.kind if subscription else None,
            subscription_start_date=str(
                subscription.start_date) if subscription else None,  # ✅ new
            subscription_end_date=str(
                subscription.end_date) if subscription else None,      # ✅ new
            session_limit=subscription.session_limit if subscription else None,
            sessions_used=subscription.sessions_used if subscription else None,
            sessions_remaining=subscription.sessions_remaining() if subscription else None,
            checked_in_at=str(checkin.created_at),
        )
