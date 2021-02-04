import asyncio
from binance_asyncio.endpoints import AccountEndpoints, MarketDataEndpoints

async def main():
    api_key = ''
    secret_key = ''

    market_data = MarketDataEndpoints(api_key=api_key)
    result = await market_data.get_klines('btcusdt', start_time="2 minutes", end_time="now")
    print(result)

    market = MarketDataEndpoints(api_key)
    response_code, response_body = await market.ping()
    print(response_code, response_body)
    
    account = AccountEndpoints(api_key=api_key, secret_key=secret_key)
    result = await account.get_account_information()
    result = await account.test_order('BNBUSDT', 'SELL', 'MARKET', quantity=1)
    print(result)
    
asyncio.run(main())