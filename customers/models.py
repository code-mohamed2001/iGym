from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    barcode = models.CharField(
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(regex=r"^\d{4}$",
                           message="Barcode must be exactly 4 digits.")
        ],
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    id_number = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{14}$",
                message="ID number must be exactly 14 digits.",
            )
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.full_name}"
    
    class Meta:
        indexes = [
            # Full-name lookups and alphabetical listings
            models.Index(fields=["full_name"], name="customer_full_name_idx"),
            # Filtering/sorting customers by creation time
            models.Index(fields=["created_at"],
                         name="customer_created_at_idx"),
            models.Index(fields=["phone"],
                         name="customer_phone_idx"),
        ]


class Subscription(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
        ("paused", "Paused"),
    )
    KIND_CHOICES = (
        ("monthly", "Monthly (unlimited)"),
        ("session_pack", "Session pack"),
        ("single visit", "Single visit")
    )
    SESSION_LIMIT_CHOICES = (
        (8, "8 sessions"),
        (12, "12 sessions"),
        (16, "16 sessions"),
    )

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
    )
    session_limit = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=SESSION_LIMIT_CHOICES,
    )
    sessions_used = models.PositiveSmallIntegerField(default=0)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="subscriptions")
    kind = models.CharField(
        max_length=20, choices=KIND_CHOICES, default="monthly")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(db_index=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.kind}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            # Most common query: a customer's subscriptions filtered by status
            # e.g. fetch all active subscriptions for a given customer
            models.Index(fields=["customer", "status"],
                         name="sub_customer_status_idx"),

            # Expiry jobs: find active subs whose end_date has passed
            # e.g. Subscription.objects.filter(status="active", end_date__lte=today)
            models.Index(fields=["status", "end_date"],
                         name="sub_status_end_date_idx"),

            # Dashboard / admin listings ordered by creation time
            models.Index(fields=["created_at"], name="sub_created_at_idx"),

            # Filtering subscriptions by kind (e.g. all session_pack subs)
            models.Index(fields=["kind"], name="sub_kind_idx"),
        ]



