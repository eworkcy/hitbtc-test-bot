import requests
import pandas as pd
import plotly.graph_objects as go
from config import BASE_URL, SYMBOL

def get_candles(limit=100):
    url = f"{BASE_URL}/public/candles/{SYMBOL}"
    params = {"period": "M5", "limit": limit}
    r = requests.get(url)
    r.raise_for_status()
    return pd.DataFrame(r.json())

df = get_candles()

# Convert types
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["open"] = df["open"].astype(float)
df["high"] = df["max"].astype(float)
df["low"] = df["min"].astype(float)
df["close"] = df["close"].astype(float)

# Strategy
df["MA5"] = df["close"].rolling(5).mean()
df["MA20"] = df["close"].rolling(20).mean()

df["signal"] = 0
df.loc[df["MA5"] > df["MA20"], "signal"] = 1
df.loc[df["MA5"] < df["MA20"], "signal"] = -1

# BUY / SELL points
buy = df[df["signal"] == 1]
sell = df[df["signal"] == -1]

# Chart
fig = go.Figure()

fig.add_candlestick(
    x=df["timestamp"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="BTC Price"
)

fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["MA5"],
    line=dict(width=1),
    name="MA 5"
))

fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["MA20"],
    line=dict(width=1),
    name="MA 20"
))

fig.add_trace(go.Scatter(
    x=buy["timestamp"],
    y=buy["close"],
    mode="markers",
    marker=dict(size=8, symbol="triangle-up"),
    name="BUY"
))

fig.add_trace(go.Scatter(
    x=sell["timestamp"],
    y=sell["close"],
    mode="markers",
    marker=dict(size=8, symbol="triangle-down"),
    name="SELL"
))

fig.update_layout(
    title="BTCUSDT – HitBTC DEMO – Strategy View",
    xaxis_title="Time",
    yaxis_title="Price",
    xaxis_rangeslider_visible=False
)

#fig.show()
fig.show(renderer="browser")


