from flask import Flask, request, render_template_string
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from strategy import get_candles, ma_strategy, macd_strategy

app = Flask(__name__)

@app.route("/")
def index():
    strategy = request.args.get("strategy", "macd")

    df = get_candles()

    if strategy == "ma":
        df = ma_strategy(df)
    else:
        df = macd_strategy(df)

    buy = df[df["signal"] == 1]
    sell = df[df["signal"] == -1]

    # === STOP LOSS / TAKE PROFIT (visual example) ===
    last_price = df["close"].iloc[-1]
    stop_loss = last_price * 0.98
    take_profit = last_price * 1.04

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3]
    )

    # ===== PRICE CHART =====
    fig.add_candlestick(
        x=df["timestamp"],
        open=df["open"].astype(float),
        high=df["max"].astype(float),
        low=df["min"].astype(float),
        close=df["close"],
        row=1, col=1,
        name="Price"
    )

    fig.add_scatter(
        x=buy["timestamp"], y=buy["close"],
        mode="markers",
        marker=dict(symbol="triangle-up", size=10),
        name="BUY",
        row=1, col=1
    )

    fig.add_scatter(
        x=sell["timestamp"], y=sell["close"],
        mode="markers",
        marker=dict(symbol="triangle-down", size=10),
        name="SELL",
        row=1, col=1
    )

    # Stop-loss & Take-profit lines
    fig.add_hline(y=stop_loss, row=1, col=1, line_dash="dot", annotation_text="SL")
    fig.add_hline(y=take_profit, row=1, col=1, line_dash="dot", annotation_text="TP")

    # ===== STRATEGY OVERLAY =====
    if strategy == "ma":
        fig.add_scatter(x=df["timestamp"], y=df["MA5"], name="MA 5", row=1, col=1)
        fig.add_scatter(x=df["timestamp"], y=df["MA20"], name="MA 20", row=1, col=1)

    # ===== MACD PANEL =====
    if strategy == "macd":
        fig.add_scatter(x=df["timestamp"], y=df["macd"], name="MACD", row=2, col=1)
        fig.add_scatter(x=df["timestamp"], y=df["signal_line"], name="Signal", row=2, col=1)
        fig.add_bar(x=df["timestamp"], y=df["histogram"], name="Histogram", row=2, col=1)

    fig.update_layout(
        title=f"BTC Strategy Dashboard ({strategy.upper()})",
        xaxis_rangeslider_visible=False
    )

    chart = fig.to_html(full_html=False)

    return render_template_string("""
    <html>
    <body>
        <h2>BTC Strategy Dashboard (HitBTC Demo)</h2>
        <form>
            <select name="strategy" onchange="this.form.submit()">
                <option value="macd" {{'selected' if strategy=='macd' else ''}}>MACD</option>
                <option value="ma" {{'selected' if strategy=='ma' else ''}}>Moving Average</option>
            </select>
        </form>
        {{ chart|safe }}
    </body>
    </html>
    """, chart=chart, strategy=strategy)

if __name__ == "__main__":
    app.run(debug=True)
