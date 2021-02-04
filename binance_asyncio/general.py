from binance_asyncio.endpoints import MarketDataEndpoints

class Client:
    def __init__(self, api_key=None, secret=None) -> None:
        self.api_key, self.secret = api_key, secret
    
    def get_market_data_endpoints(self):
        return MarketDataEndpoints(self.api_key)