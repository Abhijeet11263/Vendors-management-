from rest_framework import viewsets
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        vendor.update_performance_metrics()  # Update metrics before retrieving
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        purchase_order.vendor.update_performance_metrics()  # Update metrics after acknowledgment
        return Response({'message': 'Acknowledgment recorded.'})

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
