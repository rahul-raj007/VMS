from datetime import timedelta
from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from main.models import HistoricalPerformanceModel, PurchaseOrderModel, VendorModel
from main.serializer import (
    AcknowledgePoOrder,
    CreateListViewModelSerializer,
    CreatePurchaseOderSerializer,
    History,
    RetrivePurchaseOderSerializer,
    RetriveUpdateVendorSerializer,
    UpdatePurchaseOrderSerializer,
    VendorIdSerializer,
)
from rest_framework import status
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response

# Create your views here.


class CreateListView(APIView):
    def post(self, request):
        serialiser = CreateListViewModelSerializer(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(data=serialiser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        all_vendors = VendorModel.objects.all()
        serialise_data = CreateListViewModelSerializer(instance=all_vendors, many=True)
        return Response(data=serialise_data.data, status=status.HTTP_200_OK)


class GetSpecificVendorDetailPutListDeleteView(APIView):
    def get(self, request, vendor_id):
        vendor_details = VendorModel.objects.get(id=vendor_id)
        serialise_data = CreateListViewModelSerializer(instance=vendor_details)
        return Response(data=serialise_data.data, status=status.HTTP_200_OK)

    def put(self, request, vendor_id):
        vendor_details = VendorModel.objects.get(id=vendor_id)
        serialise_data = RetriveUpdateVendorSerializer(
            instance=vendor_details, data=request.data
        )
        if serialise_data.is_valid():
            serialise_data.save()
            return Response(data=serialise_data.data, status=status.HTTP_200_OK)
        else:
            return Response(
                data=serialise_data.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, vendor_id):
        VendorModel.objects.get(id=vendor_id).delete()
        return Response(
            data={"message": "Vendor  Deleted"},
            status=status.HTTP_200_OK,
        )


class CreatePurchasedOrderView(APIView):
    def post(self, request):
        serializer = CreatePurchaseOderSerializer(data=request.data)
        if serializer.is_valid():
            vendor_id = serializer.validated_data.get("vendor_id")
            try:
                vendor_details = VendorModel.objects.get(id=vendor_id)
            except ObjectDoesNotExist:
                error_message = {"vendor_id": vendor_id, "message": "Vendor not found"}
                return Response(data=error_message, status=status.HTTP_404_NOT_FOUND)
            else:
                unique_po_order = uuid4()
                expected_delivery_data = now() + timedelta(days=2)
                po_order_to_create = {
                    "po_number": unique_po_order,
                    "vendor": vendor_details,
                    "delivery_date": expected_delivery_data,
                    "items": serializer.validated_data.get("items"),
                    "quantity": serializer.validated_data.get("quantity"),
                }
                po_order_details = PurchaseOrderModel.objects.create(
                    **po_order_to_create
                )
                po_serializer = RetrivePurchaseOderSerializer(instance=po_order_details)
                return Response(data=po_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = VendorIdSerializer(data=request.data)
        if serializer.is_valid():
            vendor_id = serializer.validated_data.get("vendor_id")
            po_orders = PurchaseOrderModel.objects.select_related("vendor").filter(
                vendor_id=vendor_id
            )
            serialized_data = RetrivePurchaseOderSerializer(
                instance=po_orders, many=True
            )
            return Response(data=serialized_data.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDeletePurchaseOrderView(APIView):
    def get(self, request, po_id):
        try:
            po_details = PurchaseOrderModel.objects.get(id=po_id)
        except ObjectDoesNotExist:
            error_message = {"po_id": po_id, "message": "Purchase order not found"}
            return Response(data=error_message, status=status.HTTP_404_NOT_FOUND)
        else:
            serialized_data = RetrivePurchaseOderSerializer(instance=po_details)
            return Response(data=serialized_data.data, status=status.HTTP_200_OK)

    def put(self, request, po_id):
        serializer = UpdatePurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                po_obj = PurchaseOrderModel.objects.get(id=po_id)
            except ObjectDoesNotExist:
                error_message = {
                    "po_id": po_id,
                    "message": "Purcahse order Not Found",
                }
                return Response(data=error_message, status=status.HTTP_404_NOT_FOUND)
            else:
                PurchaseOrderModel.objects.filter(id=po_id).update(
                    **serializer.validated_data
                )
                po_obj.refresh_from_db()
                po_to_update = RetrivePurchaseOderSerializer(instance=po_obj)
                return Response(data=po_to_update.data, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        try:
            po_obj = PurchaseOrderModel.objects.get(id=po_id)
        except ObjectDoesNotExist:
            error_message = {
                "po_number": po_id,
                "message": "Purcahse order Not Found",
            }
            return Response(data=error_message, status=status.HTTP_404_NOT_FOUND)
        else:
            po_obj.delete()
            return Response(
                data={"message": "Purcahse order Deleted", "po_number": po_id},
                status=status.HTTP_200_OK,
            )


@api_view(http_method_names=["POST"])
def acknowledge_po(request, po_id):
    serializer = AcknowledgePoOrder(data=request.data)
    if serializer.is_valid():
        try:
            po_obj = PurchaseOrderModel.objects.get(id=po_id)
        except ObjectDoesNotExist:
            error_message = {
                "po_id": po_id,
                "message": "Purcahse order Not Found",
            }
            return Response(data=error_message, status=status.HTTP_404_NOT_FOUND)
        else:
            po_obj.acknowledgment_date = serializer.validated_data.get("ack_date_time")
            po_obj.save()
            return Response(
                data={"message": "Acknowledge", "Po_id": po_id},
                status=status.HTTP_200_OK,
            )

    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["GET"])
def get_performance_metrics(request, vendor_id):
    try:
        vndor_obj = VendorModel.objects.get(id=vendor_id)
    except ObjectDoesNotExist:
        return Response(
            data={"message": "vendor not found", "vendor_id": vendor_id},
            status=status.HTTP_404_NOT_FOUND,
        )
    else:
        dict_to_create = dict(
            vendor_id=vndor_obj.id,
            on_time_delivery_rate=vndor_obj.on_time_delivery_rate,
            quality_rating_avg=vndor_obj.quality_rating_avg,
            average_response_time=vndor_obj.average_response_time,
            fulfillment_rate=vndor_obj.fulfillment_rate,
        )
        hs_data = HistoricalPerformanceModel.objects.create(**dict_to_create)
        seria = History(instance=hs_data)
        return Response(data=seria.data, status=status.HTTP_200_OK)
