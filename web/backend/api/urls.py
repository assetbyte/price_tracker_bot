from django.urls import path
from .views import TrackingListView, TrackingDetailView

urlpatterns = [
    path("trackings/", TrackingListView.as_view(), name="tracking-list"),
    path("trackings/<int:pk>", TrackingDetailView.as_view(), name="tracking-detail",)
]