import asyncio
from binance_asyncio.websockets.streams import TickerStream

async def my_handler(message):
    print(message)

async def run_all_the_things(instance):
    await instance.subscribe("trxusdt")
    await instance.start(my_handler)

async def main():
    test = TickerStream()
    await asyncio.gather(run_all_the_things(test))

asyncio.run(main())