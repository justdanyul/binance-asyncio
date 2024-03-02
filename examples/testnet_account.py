import asyncio
from binance_asyncio.endpoints import AccountEndpoints, MarketDataEndpoints

async def main():
    api_key = '<insert your api key here>'
    secret_key = '<insert your secret key here>'

    account = AccountEndpoints(api_key=api_key, secret_key=secret_key ,uri='https://testnet.binance.vision/api/v3')
    
    # Check your balances on the test net
    code, result = await account.get_account_information()
    for asset in result['balances']:
        print("asset {}: balance = {}".format(asset['asset'], asset['free']))
    
asyncio.run(main())