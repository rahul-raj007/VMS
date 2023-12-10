from django.urls import path

from main.views import CreatePurchasedOrderView,GetUpdateDeletePurchaseOrderView,acknowledge_po

urlpatterns = [
    path("", view=CreatePurchasedOrderView.as_view()),
    path("/<int:po_id>/", view=GetUpdateDeletePurchaseOrderView.as_view()),
    path("/<int:po_id>/acknowledge", view=acknowledge_po),
]
