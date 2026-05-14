from rest_framework import serializers

from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='customer.full_name', read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Invoice
        fields = ['invoice_number', 'customer_name',
                  'amount', 'amount_after_discount', 'payment_type', 'status', 'created_at', 'created_by', 'payment_reference']
