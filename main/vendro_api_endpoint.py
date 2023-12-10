from django.urls import path
from main.views import (
    CreateListView,
    GetSpecificVendorDetailPutListDeleteView,
    get_performance_metrics,
)

urlpatterns = [
    path("", view=CreateListView.as_view()),
    path("/<int:vendor_id>/", view=GetSpecificVendorDetailPutListDeleteView.as_view()),
    path(
        "/<int:vendor_id>/performance",
        view=get_performance_metrics,
    ),
]
