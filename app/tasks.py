from typing import Literal
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import requests

from .models import Asset, PriceData

TARGET_ASSETS = ["bitcoin", "ethereum", "solana"]


@shared_task
def fetch_crypto_prices() -> Literal["Prices updated successfully"] | Literal["Failed"]:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(TARGET_ASSETS),
        "vs_currencies": "usd",
    }

    # get channel layer to talk to websockets
    channel_layer = get_channel_layer()

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # iterate through responses to save to DB
        for coin_id, prices in data.items():
            if prices.get("usd"):
                # save to database
                asset_obj, _ = Asset.objects.get_or_create(
                    symbol=coin_id.upper(), defaults={"name": coin_id.capitalize()}
                )
                price_obj = PriceData.objects.create(
                    asset=asset_obj,
                    price=prices.get("usd"),
                )
                print(f"Saved {coin_id}: ${prices.get('usd')}")

                # broadcast to websocket group
                message_data = {
                    "symbol": asset_obj.symbol,
                    "price": str(price_obj.price),
                    "timestamp": str(price_obj.timestamp),
                }
                async_to_sync(channel_layer.group_send)(
                    "crypto_feed",  # match the group name in consumers.py
                    {
                        "type": "price_update",  # match method name in consumers.py
                        "data": message_data,
                    },
                )

        return "Prices updated and broadcasted successfully"

    except requests.RequestException as e:
        print(f"API Request Failed: {e}")
        return "Failed"
