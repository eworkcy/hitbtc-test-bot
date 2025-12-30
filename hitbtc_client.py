import requests
from requests.auth import HTTPBasicAuth
from config import API_KEY, API_SECRET, BASE_URL

auth = HTTPBasicAuth(API_KEY, API_SECRET)

def get_price(symbol):
    url = f"{BASE_URL}/public/ticker/{symbol}"
    r = requests.get(url)
    r.raise_for_status()
    return float(r.json()["last"])

def get_balance(currency):
    url = f"{BASE_URL}/spot/balance"
    r = requests.get(url, auth=auth)
    r.raise_for_status()
    for b in r.json():
        if b["currency"] == currency:
            return float(b["available"])
    return 0.0

def place_order(symbol, side, quantity):
    url = f"{BASE_URL}/spot/order"
    payload = {
        "symbol": symbol,
        "side": side,
        "type": "market",
        "quantity": str(quantity)
    }
    r = requests.post(url, json=payload, auth=auth)
    r.raise_for_status()
    return r.json()
