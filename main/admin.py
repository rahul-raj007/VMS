from django.contrib import admin

from main.models import HistoricalPerformanceModel, PurchaseOrderModel, VendorModel

# Register your models here.

admin.site.register(VendorModel)
admin.site.register(PurchaseOrderModel)
admin.site.register(HistoricalPerformanceModel)
