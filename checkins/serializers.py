# checkins/serializers.py
from rest_framework import serializers
from .models import CheckIn


class CheckInSerializer(serializers.ModelSerializer):
    """
    Handles input validation and output shape only.
    No business logic here.
    """

    # write only — what comes IN from the API request
    barcode = serializers.CharField(
        write_only=True,
        required=True,
        max_length=4,
        min_length=4,
        help_text="4 digit customer barcode"
    )

    customer_barcode = serializers.CharField(      # ✅ added
        source="customer.barcode",
        read_only=True
    )

    visit_type = serializers.ChoiceField(
        choices=CheckIn.VISIT_TYPE_CHOICES,
        required=False,
        default="subscription",
        initial="subscription"
    )

    # read only — what goes OUT in the response
    customer_name = serializers.CharField(
        source="customer.full_name",
        read_only=True
    )

    

    class Meta:
        model = CheckIn
        fields = [
            "barcode",          # write only
            "customer_barcode",
            "visit_type",
            "customer_name",     # read only
      # read only
            "created_at",        # read only
        ]
        read_only_fields = ["created_at"]
