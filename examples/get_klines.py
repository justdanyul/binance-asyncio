import asyncio
from binance_asyncio.endpoints import MarketDataEndpoints

async def main():
    api_key = '<insert your api key here>'
    market_data = MarketDataEndpoints(api_key=api_key)

    # the first parameter is required, the rest are all optional and shawows the names of the binance api
    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
    code, result = await market_data.get_klines('btcusdt', interval="5m", start_time="2 hours ago", end_time="now")
    print(code, result)
    
asyncio.run(main())