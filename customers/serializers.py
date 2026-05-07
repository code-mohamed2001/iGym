from rest_framework import serializers

from .models import Customer, Subscription


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['barcode', 'full_name', 'phone']


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['barcode', 'full_name', 'phone', 'id_number', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    customer=serializers.StringRelatedField()
    class Meta:
        model = Subscription
        fields = ['customer', 'kind', 'start_date', 'end_date', 'status', 'session_limit', 'sessions_used',
                  'created_at', 'created_by']
