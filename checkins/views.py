from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CheckIn
from .serializers import CheckInSerializer


# Create your views here.
@api_view()
def checkin_list(request):
    checkin = CheckIn.objects.all()
    serializer = CheckInSerializer(checkin, many=True)
    return Response(serializer.data)


