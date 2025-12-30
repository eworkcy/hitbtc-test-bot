import time
from hitbtc_client import get_price, get_balance, place_order
from strategy import get_candles, ma_strategy, macd_strategy
import os

SYMBOL = os.getenv("SYMBOL", "BTCUSDT")


# ===== CONFIG =====
STRATEGY = "macd"   # "macd" or "ma"
BTC_AMOUNT = 0.001   # amount per trade
SLEEP_INTERVAL = 300  # seconds between checks (5 minutes)

print(f"Starting bot with {STRATEGY.upper()} strategy...")

while True:
    try:
        # 1️⃣ Get latest candles
        df = get_candles()

        # 2️⃣ Apply chosen strategy
        if STRATEGY == "ma":
            df = ma_strategy(df)
        else:
            df = macd_strategy(df)

        # 3️⃣ Get balances and price
        btc_balance = get_balance("BTC")
        usdt_balance = get_balance("USDT")
        price = get_price(SYMBOL)

        # 4️⃣ Get latest signal
        signal = df["signal"].iloc[-1]

        print(f"Price: {price} | BTC: {btc_balance} | USDT: {usdt_balance} | Signal: {signal}")

        # 5️⃣ Execute trades based on signal
        if signal == 1 and usdt_balance > price * BTC_AMOUNT:
            print("BUY signal detected!")
            order = place_order(SYMBOL, "buy", BTC_AMOUNT)
            print("Order executed:", order)

        elif signal == -1 and btc_balance >= BTC_AMOUNT:
            print("SELL signal detected!")
            order = place_order(SYMBOL, "sell", BTC_AMOUNT)
            print("Order executed:", order)

        else:
            print("No action.")

        # 6️⃣ Wait until next check
        time.sleep(SLEEP_INTERVAL)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
