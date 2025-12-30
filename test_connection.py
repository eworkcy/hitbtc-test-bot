from hitbtc_client import get_price, get_balance

print("BTC Price:", get_price("BTCUSDT"))
print("BTC Balance:", get_balance("BTC"))
print("USDT Balance:", get_balance("USDT"))
