from rest_framework import serializers

from .models import CheckIn


class CheckInSerializer(serializers.ModelSerializer):
    customer_barcode = serializers.CharField(write_only=True)
    visit_type = serializers.ChoiceField(
        choices=CheckIn.VISIT_TYPE_CHOICES,
        required=False,
        default="subscription",
        initial="subscription",
    )

    customer = serializers.CharField(source="customer.barcode", read_only=True)
    customer_full_name = serializers.CharField(
        source="customer.full_name", read_only=True)
    customer_phone = serializers.CharField(
        source="customer.phone", read_only=True)

    latest_subscription = serializers.SerializerMethodField(read_only=True)

    def get_latest_subscription(self, obj):
        if not obj.customer_id:
            return None
        sub = (
            obj.customer.subscriptions.select_related("customer")
            .order_by("-created_at")
            .first()
        )
        if sub is None:
            return None
        if sub.kind == "monthly":
            return {
                "kind": sub.kind,
                "start_date": sub.start_date,
                "end_date": sub.end_date,
            }
        if sub.kind == "session_pack":
            remaining = None
            if sub.session_limit is not None:
                remaining = max(0, sub.session_limit - sub.sessions_used)
            return {
                "kind": sub.kind,
                "start_date": sub.start_date,
                "end_date": sub.end_date,
                "remaining_sessions": remaining,
            }
        return {
            "kind": sub.kind,
            "start_date": sub.start_date,
            "end_date": sub.end_date,
        }

    class Meta:
        model = CheckIn
        fields = [
            "customer_barcode",  # input (scan)
            "customer",          # output (barcode)
            "customer_full_name",
            "customer_phone",
            "visit_type",
            "latest_subscription",
        ]
