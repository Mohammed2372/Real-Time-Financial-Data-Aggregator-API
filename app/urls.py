from django.urls import path, include

from app.views import AssetList, PriceHistoryList


urlpatterns = [
    path("assets/", AssetList.as_view(), name="asset-list"),
    path("prices/", PriceHistoryList.as_view(), name="price-history"),
]
