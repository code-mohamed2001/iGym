from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from datetime import timedelta


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
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
        related_name="created_customers",
    )

    def __str__(self):
        return f"{self.full_name}"


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
    )
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="subscriptions")
    kind = models.CharField(
        max_length=20, choices=KIND_CHOICES, default="monthly")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    session_limit = models.PositiveSmallIntegerField(
        null=True, blank=True)   # 8/12/16
    sessions_used = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.kind == "session_pack":
            if self.session_limit not in (8, 12, 16):
                raise ValidationError(
                    {"session_limit": "Session pack limit must be 8, 12, or 16."})
            # enforce “30 days from start”
            expected_end = self.start_date + timedelta(days=30)
            if self.end_date != expected_end:
                raise ValidationError(
                    {"end_date": "For session packs, end_date must equal start_date + 30 days."})
        else:
            # monthly: ensure session fields not used
            if self.session_limit is not None:
                raise ValidationError(
                    {"session_limit": "Monthly subscription must not have a session_limit."})

    @property
    def remaining_sessions(self):
        if self.kind != "session_pack":
            return None
        return max(0, (self.session_limit or 0) - self.sessions_used)

    @property
    def is_currently_active(self):
        today = timezone.localdate()
        date_ok = self.start_date <= today <= self.end_date
        status_ok = self.status == "active"
        if self.kind == "monthly":
            return status_ok and date_ok
        return status_ok and date_ok and (self.sessions_used < (self.session_limit or 0))


class Session(models.Model):
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="sessions")
    subscription = models.ForeignKey(
        "Subscription", on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions")

    started_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.full_name} @ {self.started_at:%Y-%m-%d %H:%M}"
