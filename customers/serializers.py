from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['barcode', 'full_name', 'phone', 'id_number','created_at']
