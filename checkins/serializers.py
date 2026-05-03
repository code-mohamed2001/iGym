from rest_framework import serializers

from .models import CheckIn


class CheckInSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', read_only=True)

    class Meta:
        model = CheckIn
        fields = ['customer_barcode', 'customer_name',
                  'visit_type', 'created_at', 'created_by_name']
