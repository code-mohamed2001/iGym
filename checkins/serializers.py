# checkins/serializers.py
from rest_framework import serializers
from .models import CheckIn
from core.services import CustomerService


class CheckInSerializer(serializers.ModelSerializer):
    customer_barcode = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Customer barcode to scan"
    )

    visit_type = serializers.ChoiceField(
        choices=CheckIn.VISIT_TYPE_CHOICES,
        required=False,
        default="subscription",
        initial="subscription"
    )

    # Read-only fields
    customer = serializers.CharField(source="customer.barcode", read_only=True)
    customer_full_name = serializers.CharField(
        source="customer.full_name", read_only=True)
    customer_phone = serializers.CharField(
        source="customer.phone", read_only=True)

    # Add session info to response
    session_used = serializers.BooleanField(read_only=True)
    session_message = serializers.CharField(read_only=True)
    remaining_sessions = serializers.IntegerField(
        read_only=True, allow_null=True)

    latest_subscription = serializers.SerializerMethodField(read_only=True)

    def validate_customer_barcode(self, value):
        """Validate that the customer exists"""
        if not CustomerService.customer_exists(value):
            raise serializers.ValidationError(
                f"Customer with barcode '{value}' does not exist."
            )
        return value

    def create(self, validated_data):
        """Create a new check-in and process session pack logic"""
        customer_barcode = validated_data.pop('customer_barcode')
        visit_type = validated_data.get('visit_type', 'subscription')

        # Get customer
        customer = CustomerService.get_customer_by_barcode(customer_barcode)

        if not customer:
            raise serializers.ValidationError({
                "customer_barcode": f"Customer not found"
            })

        # Process session pack logic
        session_result = CustomerService.process_checkin_session(
            customer, visit_type)

        if not session_result['success']:
            raise serializers.ValidationError({
                "checkin": session_result['message']
            })

        # Create the check-in
        checkin = CheckIn.objects.create(
            customer=customer,
            **validated_data
        )

        # Attach session result to the instance for serialization
        checkin.session_used = session_result['subscription_used']
        checkin.session_message = session_result.get('message')
        if session_result.get('subscription'):
            checkin.remaining_sessions = session_result['subscription'].get(
                'remaining_sessions')

        return checkin

    def get_latest_subscription(self, obj):
        """Get latest subscription for the customer"""
        if not obj.customer_id:
            return None

        sub = CustomerService.get_latest_subscription(obj.customer)

        if not sub:
            return None

        result = {
            "kind": sub.kind,
            "start_date": sub.start_date,
            "end_date": sub.end_date,
        }

        if sub.kind == "session_pack":
            remaining = None
            if sub.session_limit is not None:
                remaining = max(0, sub.session_limit - sub.sessions_used)
            result["remaining_sessions"] = remaining
            result["total_sessions"] = sub.session_limit
            result["used_sessions"] = sub.sessions_used

        return result

    class Meta:
        model = CheckIn
        fields = [
            "customer_barcode",
            "customer",
            "customer_full_name",
            "customer_phone",
            "visit_type",
            'created_at',
            "latest_subscription",
            "session_used",
            "session_message",
            "remaining_sessions",
        ]
