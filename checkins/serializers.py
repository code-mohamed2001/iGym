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
    customer_full_name = serializers.CharField(source="customer.full_name", read_only=True)
    customer_phone = serializers.CharField(source="customer.phone", read_only=True)

    created_by_name = serializers.CharField(source="created_by.get_full_name", read_only=True)

    class Meta:
        model = CheckIn
        fields = [
            "customer_barcode",  # input (scan)
            "customer",          # output (barcode)
            "customer_full_name",
            "customer_phone",
            "visit_type",
            "created_at",
            "created_by_name",
        ]
