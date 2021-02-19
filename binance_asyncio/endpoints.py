from binance_asyncio.requests import Request, RequestBuilder
import aiohttp
import time
import hmac
import hashlib
from urllib.parse import urlencode

class BaseClient:
    uri: str = "https://api.binance.com/api/v3"
    def __init__(self, api_key, secret_key = None) -> None:
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        if not api_key is None:
            self.headers['X-MBX-APIKEY'] = api_key
        
        self.secret_key = secret_key

    async def _get(self, endpoint: str, parameters: dict = dict(), signed=False):
        async with aiohttp.ClientSession() as session:
            if signed:
                parameters['signature'] = self.get_signature(parameters)

            query_string = urlencode(parameters)
            location = '{}/{}?{}'.format(BaseClient.uri, endpoint, query_string)
                
            async with session.get(location, headers=self.headers) as response:
                return response.status, await response.json()
    
    async def _post(self, endpoint: str, parameters: dict = dict(), signed=False):
        async with aiohttp.ClientSession() as session:
            if signed:
                parameters['signature'] = self.get_signature(parameters)

            query_string = urlencode(parameters)
            location = '{}/{}'.format(BaseClient.uri, endpoint)
            async with session.post(location, headers=self.headers, data=str.encode(query_string)) as response:
                return response.status, await response.json()

    def get_signature(self, parameters):
        request = str.encode(urlencode(parameters))
        if self.secret_key:
            return hmac.new(str.encode(self.secret_key), request, hashlib.sha256).hexdigest()
        else:
            raise Exception("Secret key required")



class GeneralEndpoints(BaseClient):
    """
    Class wrapping the general endpoints of the BINANCE RESTfull API

    :param api_key: your Binance provided API key
    :type api_key: string
    """
    def __init__(self, api_key=None) -> None:
        super().__init__(api_key)

    async def get_exchange_info(self):
        """
        Get the current exchange trading rules and symbol information

        :rtype: (int, dict)  
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element is a dict representing 
            the JSON response from the server
        """
        return await self._get('exchangeInfo')

    async def get_server_time(self):
        """
        This checks the connectivity to the binance REST APIs, and returns the current server time.
        
        :rtype: (int, dict)   
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element is a dict representing 
            the JSON response from the server of the form

            .. code-block::
            
                {
                    "serverTime": 1499828319859
                }
        """      
        return await self._get('time')

    async def ping(self):
        """
        Ping the exchange to test the connectivity to the binance REST APIs
        """          
        return await self._get('ping')


class MarketDataEndpoints(BaseClient):
    """
    Class wrapping the Market data endpoints of the BINANCE RESTfull API

    :param api_key: your Binance provided API key
    :type api_key: string
    """
    def __init__(self, api_key=None) -> None:
        super().__init__(api_key)

    async def get_orderbook(self, symbol: str, limit=100):
        """
        Gets the order book.

        :param symbol: The symbol of the pair
        :param limit: The maximum number results wanted. It default to 100 , the  
            maximum is 5000. And valid limits are 5, 10, 20, 50, 100, 500, 1000, 5000
        :type symbol: string
        :type limit: int
        :rtype: (int, dict)   
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element is a dict representing 
            the JSON response from the server

            .. code-block::
            
                {
                    "lastUpdateId": 23321024,
                    "bids": [
                        [
                        "1.00000000",    // the price
                        "42.00000000"    // the quantity
                        ]
                    ],
                    "asks": [
                        [
                        "4.00001300",
                        "14.00000000"
                        ]
                    ]
                }
        """  
        return await self._get('depth', \
            RequestBuilder().with_symbol(symbol).with_limit(limit).build().get_params())

    async def get_recent_trades(self, symbol: str, limit=500):
        """
        Get the most recent trades for a symbol.

        :param symbol: The symbol of the pair
        :param limit: The maximum number results wanted. It default to 500 , the maximum is 1000.
        :type symbol: string
        :type limit: int
        :rtype: (int, list) 
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element is a list 
            containing all recent trades 

            .. code-block::
            
                [
                    {
                        "id": 82457,
                        "price": "23.00000",
                        "qty": "12.00000000",
                        "quoteQty": "48.000012",
                        "time": 1499865542190,
                        "isBuyerMaker": true,
                        "isBestMatch": true
                    }
                ]
        """
        return await self._get('trades', \
            RequestBuilder().with_symbol(symbol).with_limit(limit).build().get_params())
    
    async def get_historical_trades(self, symbol: str, limit=500, from_id=None):
        """
        Get historical trades for a symbol.

        :param symbol: The symbol of the pair
        :param limit: The maximum number results wanted. It default to 500 , the maximum is 1000.
        :param from_id: This is the tradeid to fetch from, if none is provided, it just gets most recent trades
        :type symbol: string
        :type limit: int
        :rtype: (int, list) 
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element is a list 
            containing all recent trades 

            .. code-block::
            
                [
                    {
                        "id": 82457,
                        "price": "23.00000",
                        "qty": "12.00000000",
                        "quoteQty": "48.000012",
                        "time": 1499865542190,
                        "isBuyerMaker": true,
                        "isBestMatch": true
                    }
                ]
        """
        return await self._get('historicalTrades', 
            RequestBuilder()
                .with_symbol(symbol)
                .with_limit(limit)
                .with_from_id(from_id)
                .build()
                .get_params())


    async def get_aggregated_trades(self, symbol: str, from_id=None, start_time=None, end_time=None, limit=500):
        return await self._get('aggTrades', 
            RequestBuilder()
                .with_symbol(symbol)
                .with_limit(limit)
                .with_from_id(from_id)
                .with_start_time(start_time)
                .with_end_time(end_time)
                .build()
                .get_params())

    async def get_klines(self, symbol: str, interval='1m', start_time=None, end_time=None, limit=500):
        return await self._get('klines', RequestBuilder()
                .with_symbol(symbol)
                .with_limit(limit)
                .with_interval(interval)
                .with_start_time(start_time)
                .with_end_time(end_time)
                .build()
                .get_params())

    async def get_current_average(self, symbol: str):
        return await self._get('avgPrice',
            RequestBuilder().with_symbol(symbol).build().get_params())

    async def get_price_change_stats_ticker(self, symbol: str):
        return await self._get('ticker/24hr', 
            RequestBuilder().with_symbol(symbol).build().get_params())

    async def get_symbol_price_ticker(self, symbol: str):
        return await self._get('ticker/price', 
            RequestBuilder().with_symbol(symbol).build().get_params())

    async def get_symbol_order_book_ticker(self, symbol: str):
        return await self._get('ticker/bookTicker', 
            RequestBuilder().with_symbol(symbol).build().get_params())


class AccountEndpoints(BaseClient):
    async def get_account_information(self):
        return await self._get('account', 
            RequestBuilder()
                .with_timestamp()
                .build()
                .get_params(),
            True)

    async def _create_order(self, symbol: str, side:str, order_type:str, **parameters):
        timestamp = int(round(time.time() * 1000))
        request = Request()
        request.add_param('symbol', symbol)
        request.add_param('side', side)
        request.add_param('type', order_type)
        request.add_param('timestamp', timestamp)
        request.add_parameters(parameters)
        return request

    async def test_order(self, symbol: str, side:str, order_type:str, **parameters):
        request = await self._create_order(symbol, side, order_type, **parameters)
        return await self._post('order/test', request.get_params(), True)

    async def order(self, symbol: str, side:str, order_type:str, **parameters):
        request = await self._create_order(symbol, side, order_type, **parameters)
        return await self._post('order', request.get_params(), True)

