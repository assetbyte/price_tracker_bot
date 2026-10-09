from django.urls import path
from .views import (TrackingListView,
                    TrackingDetailView, 
                    PriceHistoryView,
                    StationSearchView,
                    )

urlpatterns = [
    path("trackings/", TrackingListView.as_view(), name="tracking-list"),
    path("trackings/<int:pk>/", TrackingDetailView.as_view(), name="tracking-detail",),
    path("trackings/<int:pk>/price-history/", PriceHistoryView.as_view(), name="price-history"),
    path('stations/', StationSearchView.as_view(), name='station-search'),
]
