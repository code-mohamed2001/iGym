from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Invoice
from .serializers import InvoiceSerializer


# Create your views here.
@api_view()
def invoice_list(request):
    invoice = Invoice.objects.all()
    serializer = InvoiceSerializer(invoice, many=True)
    return Response(serializer.data)
