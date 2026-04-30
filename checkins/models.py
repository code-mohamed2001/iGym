from django.conf import settings
from django.db import models

# Create your models here.


class CheckIn(models.Model):
    customer = models.ForeignKey(
        "customers.Customer", related_name='checkins', on_delete=models.PROTECT,
        db_index=True)

    VISIT_TYPE_CHOICES = (
        ("walk_in", "Walk-in"),
        ("free_trial", "Free trial"),
        ("subscription", "Subscription")
    )
    visit_type = models.CharField(
        max_length=20, choices=VISIT_TYPE_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_customers",
    )
