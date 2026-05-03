from rest_framework import serializers

from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='customer.full_name', read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'customer_name', 'subscription',
                  'amount', 'payment_type', 'status', 'created_at', 'created_by', 'payment_reference']
