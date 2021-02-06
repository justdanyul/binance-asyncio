import asyncio
from binance_asyncio.websockets.streams import KlineStream

async def my_handler(message):
    print(message)

async def main():
    stream = KlineStream()

    # takes two parameters, the symbol and the chart interval
    # for meaning of chart intervals, see:
    # https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams
    await stream.subscribe("trxusdt", "5m")
    await stream.subscribe("btcusdt", "5m") # you can stack them if you want
    await stream.start(my_handler)

asyncio.run(main())