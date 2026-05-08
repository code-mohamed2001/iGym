from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Customer, Subscription
from .serializers import (
    CustomerDetailSerializer,
    CustomerSerializer,
    SubscriptionSerializer,
)


# Create your views here.
@api_view()
def customer_list(request):
    customer = Customer.objects.select_related('created_by').all()
    serializer = CustomerSerializer(customer, many=True)
    return Response(serializer.data)


@api_view()
def customer_datail(request, id):
    customer = get_object_or_404(Customer, barcode=id)
    serializer = CustomerDetailSerializer(customer)
    return Response(serializer.data)


@api_view()
def subscription_list(request):
    subs = Subscription.objects.select_related('customer').select_related('created_by').all()
    serializer = SubscriptionSerializer(subs, many=True)
    return Response(serializer.data)
