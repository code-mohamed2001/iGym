# apps/payments/models.py
import random
import string

from django.conf import settings
from django.db import models


def generate_invoice_number():
    while True:
        number = ''.join(random.choices(string.digits, k=6))
        invoice_number = f"INV-{number}"
        if not Invoice.objects.filter(invoice_number=invoice_number).exists():
            return invoice_number


class Invoice(models.Model):
    # Payment Status Choices
    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('waiting_approval', 'Waiting for Approval'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )

    # Payment Type Choices
    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Cash'),
        ('vodafone_cash', 'Vodafone Cash'),
        ('instapay', 'Instapay'),
        ('bank_transfer', 'Bank Transfer'),  # Added for future
        ('credit_card', 'Credit Card'),       # Added for future
    )

    SUBSCRIBTION_KIND_CHOICES = (
        ("monthly", "Monthly (unlimited)"),
        ("session_pack", "Session pack"),
        ("single visit", "Single visit")
    )

    invoice_number = models.CharField(
        max_length=10,
        unique=True,
        blank=True,  # so we can auto-fill it before saving
        editable=False,
    )

    # Relationships
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        related_name='invoices',
        db_index=True
    )

    subscription = models.CharField(
        max_length=20,
        choices=SUBSCRIBTION_KIND_CHOICES,
        null=False,
        default='monthly'
    )

    # Financial Fields
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Invoice amount in EGP"
    )

    # Payment Tracking
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        default='cash'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unpaid',
        db_index=True
    )

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)

    # Audit Trail
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_invoices',
        db_index=True
    )

    # Additional Fields
    payment_reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="Transaction ID or reference number from payment provider"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['payment_type', 'status']),
        ]

    def __str__(self):
        return f"{self.id} - {self.customer.full_name} - {self.status}"

    @property
    def is_paid(self):
        """Check if invoice is paid"""
        return self.status == 'paid'

    def save(self, *args, **kwargs):
        if not self.invoice_number:  # only generate if not already set
            self.invoice_number = generate_invoice_number()
        super().save(*args, **kwargs)
