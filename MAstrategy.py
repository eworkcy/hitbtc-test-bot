import requests
import pandas as pd
from config import BASE_URL, SYMBOL

def get_candles(limit=50):
    url = f"{BASE_URL}/public/candles/{SYMBOL}"
    params = {"period": "M5", "limit": limit}
    r = requests.get(url, params=params)
    r.raise_for_status()
    closes = [float(c["close"]) for c in r.json()]
    return pd.Series(closes)

def should_buy():
    prices = get_candles()
    return prices.rolling(5).mean().iloc[-1] > prices.rolling(20).mean().iloc[-1]

def should_sell():
    prices = get_candles()
    return prices.rolling(5).mean().iloc[-1] < prices.rolling(20).mean().iloc[-1]
