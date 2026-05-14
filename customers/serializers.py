from django.utils import timezone
from rest_framework import serializers

from core import invoice_constants

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

    invoice_status = serializers.ChoiceField(
        choices=invoice_constants.INVOICE_STATUS_CHOICES,
        required=False,
        default=invoice_constants.DEFAULT_INVOICE_STATUS,
        write_only=True,
    )
    amount_after_discount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
        write_only=True,
    )
    payment_type = serializers.ChoiceField(
        choices=invoice_constants.PAYMENT_TYPE_CHOICES,
        required=False,
        default=invoice_constants.DEFAULT_PAYMENT_TYPE,
        write_only=True,
    )
    payment_reference = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        max_length=100,
        write_only=True,
    )

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

    def update(self, instance, validated_data):
        validated_data.pop("invoice_status", None)
        validated_data.pop("amount_after_discount", None)
        validated_data.pop("payment_type", None)
        validated_data.pop("payment_reference", None)
        return super().update(instance, validated_data)

    class Meta:
        model = Subscription
        fields = [
            "customer",
            "customer_display",
            "kind",
            "price",
            "start_date",
            "end_date",
            "status",
            "session_limit",
            "sessions_used",
            "created_at",
            "created_by",
            "invoice_number",
            "invoice_status",
            "amount_after_discount",
            "payment_type",
            "payment_reference",
        ]
