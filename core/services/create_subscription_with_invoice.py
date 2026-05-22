from __future__ import annotations

from typing import Any

from django.db import transaction

from core import invoice_constants
from core.utilities import generate_unique_invoice_number
from customers.models import Subscription
from payments.models import Invoice


def create_subscription_with_invoice(
    *,
    created_by: Any,
    customer: Any,
    kind: str,
    price: Any,
    start_date: Any,
    end_date: Any,
    session_limit: int | None = None,
    sessions_used: int = 0,
    invoice_status: str = invoice_constants.DEFAULT_INVOICE_STATUS,
    amount_after_discount: Any | None = None,
    payment_type: str = invoice_constants.DEFAULT_PAYMENT_TYPE,
    payment_reference: str = "",
) -> Subscription:
    """
    Create a Subscription and matching Invoice; both share the same
    invoice_number (assigned before save).
    """
    invoice_number = generate_unique_invoice_number()
    after_discount = (
        price if amount_after_discount is None else amount_after_discount
    )
    with transaction.atomic():
        subscription = Subscription.objects.create(
            customer=customer,
            kind=kind,
            price=price,
            start_date=start_date,
            end_date=end_date,
            session_limit=session_limit,
            sessions_used=sessions_used,
            invoice_number=invoice_number,
            created_by=created_by,
        )
        Invoice.objects.create(
            customer=customer,
            amount=price,
            amount_after_discount=after_discount,
            subscription=kind,
            created_by=created_by,
            invoice_number=invoice_number,
            status=invoice_status,
            payment_type=payment_type,
            payment_reference=payment_reference,
        )
    return subscription
