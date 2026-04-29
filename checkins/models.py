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
    subscription = models.ForeignKey(
        "customers.Subscription", null=True, blank=True,  on_delete=models.SET_NULL, related_name='checkins')
    visit_type = models.CharField(
        max_length=20, choices=VISIT_TYPE_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_customers",
    )
