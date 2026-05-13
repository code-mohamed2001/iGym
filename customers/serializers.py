from django.utils import timezone
from rest_framework import serializers

from .models import Customer, Subscription


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['barcode', 'full_name', 'phone', 'id_number']


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['barcode', 'full_name', 'phone', 'id_number', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all())
    customer_display = serializers.StringRelatedField(
        source="customer", read_only=True)  # read: __str__

    created_by = serializers.StringRelatedField(read_only=True)
    invoice_number = serializers.CharField(read_only=True)
    status = serializers.SerializerMethodField(
        method_name='check_subscription_status')
    
    

    def check_subscription_status(self, obj):
        if obj.end_date < timezone.now().date():
            return "expired"
        elif obj.kind == "session_pack":
            if obj.session_limit == obj.sessions_used:
                return "expired"
            else:
                return "active"
        else:
            return "active"

    class Meta:
        model = Subscription
        fields = ['customer', "customer_display", 'kind', "price", 'start_date', 'end_date', 'status', 'session_limit', 'sessions_used',
                  'created_at', 'created_by','invoice_number']
