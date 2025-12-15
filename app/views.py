from rest_framework import generics
from django_filters import rest_framework as filters

from .models import Asset, PriceData
from .serializers import AssetSerializer, PriceDataSerializer


# Create your views here.
class PriceFilter(filters.FilterSet):
    # filter by symbol
    symbol = filters.CharFilter(field_name="asset__symbol", lookup_expr="iexact")

    # filter by date range
    from_date = filters.DateFilter(field_name="timestamp", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = PriceData
        fields = ["symbol", "from_date", "to_date"]


class AssetList(generics.ListAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class PriceHistoryList(generics.ListAPIView):
    queryset = PriceData.objects.all()
    serializer_class = PriceDataSerializer
    filterset_class = PriceFilter
