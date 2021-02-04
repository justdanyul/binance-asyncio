Getting started
===============

Firstly, install the package with

.. code-block:: console

    pip install binance-asyncio

Making your first request
-------------------------
Lets say you want to retrieve all klines, with interval length of 1 minute,from the last 10 minutes. You then simply

.. code-block::

    import asyncio
    from binance_asyncio.endpoints.market_data import MarketDataEndpoints

    async def main():
        secret_key = 'insert key here'
        my_api_key = 'insert key here'
        market_data = MarketDataEndpoints(api_key=my_api_key)
        general_endpoints = get_general_endpoint()
        result = await market_data.get_klines('btcusdt', interval="1m", start_time="10 minutes ago")
        print(result)

    asyncio.run(main())

The two main learnings of this short example are

- You must provide your api key and secret
- We use the BinanceClient to get an configured instance of the class ``MarketDataEndpoints``, which encapsulate all interaction with BINANCE's RESTfull market data endpoints

You can use BinanceClient to get instances of

- :class:`binance_asyncio.endpoints.market_data.MarketDataEndpoints`
- :class:`binance_asyncio.endpoints.market_data.MarketDataEndpoints`

To learn more about information about the individual classes visit  
and the binance api documentation.