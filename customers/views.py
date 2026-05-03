from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Customer,Subscription
from .serializers import CustomerSerializer



# Create your views here.
@api_view()
def customer_list(request):
    customer=Customer.objects.all()
    serializer=CustomerSerializer(customer,many=True)
    return Response(serializer.data)

@api_view()
def customer_datail(request, id):
    return Response(id)
