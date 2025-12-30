import requests
import pandas as pd
from config import BASE_URL, SYMBOL

# MACD parameters (standard)
FAST = 12
SLOW = 26
SIGNAL = 9

def get_candles(limit=200):
    url = f"{BASE_URL}/public/candles/{SYMBOL}"
    params = {"period": "M5", "limit": limit}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return pd.DataFrame(r.json())

def calculate_macd(df):
    df["close"] = df["close"].astype(float)

    # EMA calculations
    df["ema_fast"] = df["close"].ewm(span=FAST, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=SLOW, adjust=False).mean()

    # MACD
    df["macd"] = df["ema_fast"] - df["ema_slow"]
    df["signal"] = df["macd"].ewm(span=SIGNAL, adjust=False).mean()
    df["histogram"] = df["macd"] - df["signal"]

    return df

def should_buy():
    df = get_candles()
    df = calculate_macd(df)

    # MACD crosses ABOVE signal line
    return (
        df["macd"].iloc[-2] < df["signal"].iloc[-2]
        and df["macd"].iloc[-1] > df["signal"].iloc[-1]
    )

def should_sell():
    df = get_candles()
    df = calculate_macd(df)

    # MACD crosses BELOW signal line
    return (
        df["macd"].iloc[-2] > df["signal"].iloc[-2]
        and df["macd"].iloc[-1] < df["signal"].iloc[-1]
    )
