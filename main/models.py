from django.db import models
from django.db.models import Avg, Case, ExpressionWrapper, F, Q, When
from django.db.models.functions import Coalesce

# Create your models here.


class VendorModel(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    def __str__(self):
        return f"{self.name} {self.id}"


class Status(models.TextChoices):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class PurchaseOrderModelManager(models.Manager):
    def calculate_avg_reponse_time(self, vendor_id):
        query_filter = Q(vendor_id=vendor_id) & Q(acknowledgment_date__isnull=False)
        av_time = (
            self.get_queryset()
            .filter(query_filter)
            .annotate(
                time_diff=ExpressionWrapper(
                    F("acknowledgment_date") - F("issue_date"),
                    output_field=models.DurationField(),
                )
            )
            .aggregate(avg_time=Avg(F("time_diff")))
        )
        return av_time.get("avg_time").total_seconds()

    def get_av_rating_fll_rate(self, vendor_id):
        query_filter = Q(vendor_id=vendor_id) & Q(status=Status.completed)
        query_response = self.get_queryset().filter(query_filter)
        avg_rating = query_response.annotate(
            rate=Case(
                When(quality_rating__isnull=False, then=F("quality_rating")),
                default=0,
                output_field=models.FloatField(),
            )
        ).aggregate(rating=Avg(F("rate")))
        completed_count = query_response.count()
        total_po = self.get_queryset().filter(vendor_id=vendor_id).count()
        try:
            fl_rate = completed_count / total_po
        except ZeroDivisionError:
            fl_rate = 0.0

        dl_rate = self.get_ontime_devlivery(vendor_id,completed_count)

        return avg_rating.get("rating"), fl_rate,dl_rate

    def get_ontime_devlivery(self, vendor_id, completed_order_count):
        query_filter = (
            Q(vendor_id=vendor_id)
            & Q(status=Status.completed)
            & Q(delivery_date__date__lte=F("delivery_date"))
        )
        time_deli_count = self.get_queryset().filter(query_filter).count()
        try:
            dl_rate = time_deli_count / completed_order_count
        except ZeroDivisionError:
            dl_rate = 0.0
        return dl_rate


class PurchaseOrderModel(models.Model):
    po_number = models.CharField(max_length=200, unique=True)
    vendor = models.ForeignKey(VendorModel, on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.pending
    )
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)

    objects = PurchaseOrderModelManager()


class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
