import random
import string


def generate_unique_invoice_number() -> str:
    """Return a unique INV-###### value unused by Invoice or Subscription."""
    from customers.models import Subscription
    from payments.models import Invoice

    while True:
        digits = "".join(random.choices(string.digits, k=6))
        invoice_number = f"INV-{digits}"
        if not Invoice.objects.filter(invoice_number=invoice_number).exists():
            if not Subscription.objects.filter(
                invoice_number=invoice_number
            ).exists():
                return invoice_number
