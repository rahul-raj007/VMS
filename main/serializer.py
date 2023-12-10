from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from main.models import PurchaseOrderModel, Status, VendorModel,HistoricalPerformanceModel


class CreateListViewModelSerializer(ModelSerializer):
    class Meta:
        model = VendorModel
        fields = "__all__"
        read_only_fields = [
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]


class RetriveUpdateVendorSerializer(CreateListViewModelSerializer):
    class Meta:
        model = CreateListViewModelSerializer.Meta.model
        fields = CreateListViewModelSerializer.Meta.fields


class CreatePurchaseOderSerializer(Serializer):
    vendor_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    items = serializers.JSONField()


class RetrivePurchaseOderSerializer(ModelSerializer):
    vendor = CreateListViewModelSerializer()

    class Meta:
        model = PurchaseOrderModel
        fields = "__all__"


class VendorIdSerializer(serializers.Serializer):
    vendor_id = serializers.IntegerField()


class UpdatePurchaseOrderSerializer(Serializer):
    po_number = serializers.CharField(max_length=200)
    vendor_id = serializers.IntegerField()
    delivery_date = serializers.DateTimeField(allow_null=True, required=False)
    items = serializers.JSONField()
    quantity = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Status.choices, default=Status.pending)
    quality_rating = serializers.FloatField(allow_null=True, required=False)


class AcknowledgePoOrder(Serializer):
    ack_date_time = serializers.DateTimeField()


class History(ModelSerializer):
    class Meta:
        model=HistoricalPerformanceModel
        fields = "__all__"