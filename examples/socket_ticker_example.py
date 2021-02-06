import asyncio
from binance_asyncio.websockets.streams import TickerStream

async def my_handler(message):
    print(message)

async def main():
    stream = TickerStream()
    await stream.subscribe("trxusdt")
    await stream.subscribe("btcusdt")
    await stream.start(my_handler)

asyncio.run(main())