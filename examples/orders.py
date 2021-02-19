import asyncio
from binance_asyncio.endpoints import AccountEndpoints

async def main():
    api_key = '<insert your api key here>'
    secret_key = '<insert your secret key here>'

    account = AccountEndpoints(api_key=api_key, secret_key=secret_key)
    
    # The test_order method is simply for testing, it will provide an empty response 
    # and a 200 response code if the order request is valid. But the order
    # will not be executed.
    #
    # The first 3 parameters are required. The rest of the parameters are 
    # simply shadowning the binance api (see binance api docs for more).
    code, result = await account.test_order('BNBUSDT', 'SELL', 'MARKET', quantity=1)
    print(code, result)


    # Like the test order method, but, executes the order!
    code, result = await account.order('BNBUSDT', 'BUY', 'MARKET', quoteOrderQty=10)
    print(code, result)
    
asyncio.run(main())