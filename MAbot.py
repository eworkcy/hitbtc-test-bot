import time
from hitbtc_client import get_price, get_balance, place_order
from strategy import should_buy, should_sell
from config import SYMBOL

BTC_AMOUNT = 0.01  # demo size

while True:
    price = get_price(SYMBOL)
    btc = get_balance("BTC")
    usdt = get_balance("USDT")

    print(f"Price: {price} | BTC: {btc} | USDT: {usdt}")

    if should_buy() and usdt > price * BTC_AMOUNT:
        print("BUY (demo)")
        place_order(SYMBOL, "buy", BTC_AMOUNT)

    elif should_sell() and btc >= BTC_AMOUNT:
        print("SELL (demo)")
        place_order(SYMBOL, "sell", BTC_AMOUNT)

    time.sleep(300)
