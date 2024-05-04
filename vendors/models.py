from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    def update_performance_metrics(self):
        completed_orders = self.purchase_orders.filter(status='completed')
        total_orders = completed_orders.count()

        if total_orders > 0:
            # On-Time Delivery Rate
            on_time_deliveries = completed_orders.filter(delivery_date__lte=models.F('delivery_date')).count()
            self.on_time_delivery_rate = (on_time_deliveries / total_orders) * 100

            # Quality Rating Average
            self.quality_rating_avg = completed_orders.aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating']

            # Average Response Time
            response_times = completed_orders.exclude(acknowledgment_date__isnull=True) \
                .annotate(response_time=models.F('acknowledgment_date') - models.F('issue_date')) \
                .aggregate(avg_response=models.Avg('response_time'))['avg_response']
            self.average_response_time = response_times.total_seconds() / total_orders if response_times else 0

            # Fulfilment Rate
            successful_orders = completed_orders.filter(quality_rating__isnull=False)
            self.fulfillment_rate = (successful_orders.count() / total_orders) * 100

        self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performances')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
