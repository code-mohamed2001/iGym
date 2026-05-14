"""Invoice field choices and defaults shared by payments and customer-facing APIs."""

INVOICE_STATUS_CHOICES = (
    ("paid", "Paid"),
    ("unpaid", "Unpaid"),
    ("waiting_approval", "Waiting for Approval"),
    ("cancelled", "Cancelled"),
    ("refunded", "Refunded"),
)

PAYMENT_TYPE_CHOICES = (
    ("cash", "Cash"),
    ("vodafone_cash", "Vodafone Cash"),
    ("instapay", "Instapay"),
    ("bank_transfer", "Bank Transfer"),
    ("credit_card", "Credit Card"),
)

DEFAULT_INVOICE_STATUS = "unpaid"
DEFAULT_PAYMENT_TYPE = "cash"
