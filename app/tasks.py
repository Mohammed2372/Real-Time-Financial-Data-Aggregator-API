from celery import shared_task

import requests

from .models import Asset, PriceData

TARGET_ASSETS = ["bitcoin", "ethereum", "solana"]


@shared_task
def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(TARGET_ASSETS),
        "vs_currencies": "usd",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # iterate through responses to save to DB
        for coin_id, prices in data.items():
            if prices.get("usd"):
                asset_obj, created = Asset.objects.get_or_create(
                    symbol=coin_id.upper(), defaults={"name": coin_id.capitalize()}
                )
                PriceData.objects.create(
                    asset=asset_obj,
                    price=prices.get("usd"),
                )
                print(f"Saved {coin_id}: ${prices.get('usd')}")
        return "Prices updated successfully"

    except requests.RequestException as e:
        print(f"API Request Failed: {e}")
        return "Failed"
