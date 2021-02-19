Getting started
===============

Firstly, install the package with

.. code-block:: console

    pip install binance-asyncio

Making your first request
-------------------------
Lets say you want to retrieve all klines, with interval length of 5 minutes, from the last 2 hours. You then simply

.. code-block::

    import asyncio
    from binance_asyncio.endpoints import MarketDataEndpoints

    async def main():
        api_key = '<insert your api key here>'
        market_data = MarketDataEndpoints(api_key=api_key)
        code, result = await market_data.get_klines('btcusdt', interval="5m", start_time="2 hours ago", end_time="now")
        print(code, result)
        
    asyncio.run(main())

The two main learnings of this short example are

- You must always provide your api key (and secret if required) when creating a new instance of an endpoint
- When providing time parameters, such as ``start_time``, you use natural language. For example, `6 seconds ago`, `1 month ago` etc.  
- All method calls, wrapping binance endpoints, will return a tuple with the response code as the first element, and the body of the response as the second
- All enums, such as the input for the interval parameter, follows `the binance documentation <https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#enum-definitions>`_

