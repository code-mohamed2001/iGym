from django.conf import settings
from django.db import models

# Create your models here.


class CheckIn(models.Model):

    VISIT_TYPE_CHOICES = (
        ("walk_in", "Walk-in"),
        ("free_trial", "Free trial"),
        ("subscription", "Subscription")
    )

    customer = models.ForeignKey(
        "customers.Customer", related_name='checkins', on_delete=models.PROTECT,
        db_index=True)

    customer_barcode = models.CharField(
        max_length=4,
        db_index=True,
        null=True
    )
    visit_type = models.CharField(
        max_length=20, choices=VISIT_TYPE_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_customers",
    )

    class Meta:
        indexes = [
            # Core lookup: all check-ins for a specific customer, newest first
            # e.g. customer visit history page
            models.Index(fields=["customer", "-created_at"],
                         name="checkin_customer_date_idx"),

            # Attendance reports filtered by date range across all customers
            # e.g. "how many check-ins happened this week?"
            models.Index(fields=["created_at"], name="checkin_created_at_idx"),

            # Barcode scan at the door: resolve customer + check recency together
            models.Index(
                fields=["customer_barcode", "-created_at"], name="checkin_barcode_date_idx"),

            # Filter check-ins by visit type, e.g. count all free trials this month
            models.Index(fields=["visit_type", "created_at"],
                         name="checkin_visit_type_date_idx"),
        ]
