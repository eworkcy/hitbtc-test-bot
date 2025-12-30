import requests
import pandas as pd
import os

BASE_URL = os.getenv("HITBTC_BASE_URL", "https://api.demo.hitbtc.com/api/3")
SYMBOL = os.getenv("SYMBOL", "BTCUSDT")

# ===== COMMON =====
def get_candles(limit=200):
    url = f"{BASE_URL}/public/candles/{SYMBOL}"
    params = {"period": "M5", "limit": limit}
    r = requests.get(url, params=params)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["close"] = df["close"].astype(float)
    return df

# ===== MA STRATEGY =====
def ma_strategy(df):
    df["MA5"] = df["close"].rolling(5).mean()
    df["MA20"] = df["close"].rolling(20).mean()

    df["signal"] = 0
    df.loc[df["MA5"] > df["MA20"], "signal"] = 1
    df.loc[df["MA5"] < df["MA20"], "signal"] = -1
    return df

# ===== MACD STRATEGY =====
def macd_strategy(df):
    df["ema_fast"] = df["close"].ewm(span=12, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = df["ema_fast"] - df["ema_slow"]
    df["signal_line"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["histogram"] = df["macd"] - df["signal_line"]

    df["signal"] = 0
    df.loc[df["macd"] > df["signal_line"], "signal"] = 1
    df.loc[df["macd"] < df["signal_line"], "signal"] = -1
    return df
