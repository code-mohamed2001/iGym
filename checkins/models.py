# checkins/models.py
from django.conf import settings
from django.db import models


class CheckIn(models.Model):

    VISIT_TYPE_CHOICES = (
        ("walk_in", "Walk-in"),
        ("free_trial", "Free trial"),
        ("subscription", "Subscription")
    )

    
    customer = models.ForeignKey(
        "customers.Customer",
        related_name='checkins',
        on_delete=models.PROTECT,
        db_index=True
    )
    visit_type = models.CharField(
        max_length=20,
        choices=VISIT_TYPE_CHOICES,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        # ✅ fixed — was "created_customers" which is wrong
        related_name="created_checkins",
    )

    class Meta:
        indexes = [
            models.Index(fields=["customer", "-created_at"],
                         name="checkin_customer_date_idx"),
            models.Index(fields=["created_at"],
                         name="checkin_created_at_idx"),
            models.Index(fields=["visit_type", "created_at"],
                         name="checkin_visit_type_date_idx"),
        ]
