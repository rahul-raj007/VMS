from main.models import PurchaseOrderModel, VendorModel


def update_historicaldata(sender, instance, created, *args, **kwargs):
    vendor_id = instance.vendor_id
    avr_res_time = PurchaseOrderModel.objects.calculate_avg_reponse_time(
        vendor_id=vendor_id
    )
    rating, fll_rate, dl_rate = PurchaseOrderModel.objects.get_av_rating_fll_rate(
        vendor_id=vendor_id
    )
    vendor_obj = VendorModel.objects.get(id=vendor_id)
    vendor_obj.on_time_delivery_rate = dl_rate
    vendor_obj.quality_rating_avg = rating if rating else 0.0
    vendor_obj.average_response_time = avr_res_time
    vendor_obj.fulfillment_rate = fll_rate
    vendor_obj.save()
