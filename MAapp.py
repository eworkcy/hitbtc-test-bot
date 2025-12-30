from flask import Flask, render_template_string
import requests
import pandas as pd
import plotly.graph_objects as go
from config import BASE_URL, SYMBOL

app = Flask(__name__)

def get_candles(limit=100):
    url = f"{BASE_URL}/public/candles/{SYMBOL}"
    params = {"period": "M5", "limit": limit}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return pd.DataFrame(r.json())

@app.route("/")
def index():
    df = get_candles()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["open"] = df["open"].astype(float)
    df["high"] = df["max"].astype(float)
    df["low"] = df["min"].astype(float)
    df["close"] = df["close"].astype(float)

    # Strategy
    df["MA5"] = df["close"].rolling(5).mean()
    df["MA20"] = df["close"].rolling(20).mean()

    buy = df[df["MA5"] > df["MA20"]]
    sell = df[df["MA5"] < df["MA20"]]

    fig = go.Figure()

    fig.add_candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="BTC"
    )

    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["MA5"], name="MA 5"
    ))

    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["MA20"], name="MA 20"
    ))

    fig.add_trace(go.Scatter(
        x=buy["timestamp"], y=buy["close"],
        mode="markers", marker=dict(symbol="triangle-up", size=8),
        name="BUY"
    ))

    fig.add_trace(go.Scatter(
        x=sell["timestamp"], y=sell["close"],
        mode="markers", marker=dict(symbol="triangle-down", size=8),
        name="SELL"
    ))

    fig.update_layout(
        title="BTCUSDT – HitBTC DEMO – Strategy",
        xaxis_rangeslider_visible=False
    )

    chart_html = fig.to_html(full_html=False)

    return render_template_string("""
        <html>
        <head><title>HitBTC Strategy Dashboard</title></head>
        <body>
            <h2>BTC Strategy View (Demo)</h2>
            {{ chart|safe }}
        </body>
        </html>
    """, chart=chart_html)

if __name__ == "__main__":
    app.run(debug=True)
