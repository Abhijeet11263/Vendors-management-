from rest_framework import routers
from .views import VendorViewSet, PurchaseOrderViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]