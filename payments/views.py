from rest_framework.viewsets import ReadOnlyModelViewSet,ModelViewSet

from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.select_related("customer", "created_by").all()
    serializer_class = InvoiceSerializer
    lookup_field = "invoice_number"
