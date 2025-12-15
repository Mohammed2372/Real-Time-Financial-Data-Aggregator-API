from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Asset, PriceData


class AssetSerializer(ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "symbol", "name", "is_active"]


class PriceDataSerializer(ModelSerializer):
    symbol = serializers.ReadOnlyField(source="asset.symbol")

    class Meta:
        model = PriceData
        fields = ["id", "symbol", "price", "timestamp"]
