from django.urls import path
from .views import TrackingListView

urlpatterns = [
    path("trackings/", TrackingListView.as_view(), name="tracking-list"),
]