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
        """
        Get aggregate trades.

        :param symbol: The symbol of the pair
        :param limit: The maximum number results wanted. It default to 500 , the maximum is 1000.
        :param from_id: This is the tradeid to get aggregate trades from (inclusive), if none is provided, it just gets most recent trades
        :param start_time: The time to begin the aggregation from. For example, '10 minutes ago' or '1 second ago'
        :param end_time: The time to end the aggregation, in similar format as above
        :type symbol: string
        :type limit: int
        :type start_time: string
        :type end_time: string
        :rtype: (int, list) 
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element is a list 
            containing the aggregated trades

            .. code-block::
            
                [
                    {
                        "a": 16239,         // agg tradeId
                        "p": "0.01633102",  // price
                        "q": "6.73443515",  // quantity
                        "f": 13781,         // the first tradeId
                        "l": 13781,         // the last tradeId
                        "T": 1498794537053, // timestamp
                        "m": true,          // is the buyer the maker?
                        "M": true           // was the trade the best price match?
                    }
                ]
        """
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
        """
        Get kline/candlestick bars for a symbol

        :param symbol: The symbol of the pair
        :param interval: The interval of the kline, valid intervals are

            - "1m"
            - "3m"
            - "5m"
            - "15m"
            - "30m"
            - "1h"
            - "2h"
            - "4h"
            - "6h"
            - "8h"
            - "12h"
            - "1d"
            - "3d"
            - "1w"
            - "1M"           
        
        :param limit: The maximum number of klines wanted. It default to 500 , the maximum is 1000.
        :param start_time: The time to get klines from from. For example, '10 minutes ago' or '1 second ago'
        :param end_time: The time to get klines until, in similar format as above
        :type symbol: string
        :type limit: int
        :type interval: string
        :type start_time: string
        :type end_time: string
        :rtype: (int, list) 
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element is a list 
            containing the klines

            .. code-block::
            
                [
                    [
                        1499040000000,      // Open time
                        "0.01634790",       // Open
                        "0.80000000",       // High
                        "0.01575800",       // Low
                        "0.01577100",       // Close
                        "148976.11427815",  // Volume
                        1499644799999,      // Close time
                        "2434.19055334",    // Quote asset volume
                        308,                // Number of trades
                        "1756.87402397",    // Taker buy base asset volume
                        "28.46694368",      // Taker buy quote asset volume
                        "17928899.62484339" // Ignore.
                    ]
                ]
        """        
        return await self._get('klines', RequestBuilder()
                .with_symbol(symbol)
                .with_limit(limit)
                .with_interval(interval)
                .with_start_time(start_time)
                .with_end_time(end_time)
                .build()
                .get_params())

    async def get_current_average(self, symbol: str):
        """
        Get the current average price for a symbol.

        :param symbol: The symbol of the pair
        :type symbol: string
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element dictionary representing the response

            .. code-block::
            
                {
                    "mins": 5,
                    "price": "9.35751834"
                }
        """        
        return await self._get('avgPrice',
            RequestBuilder().with_symbol(symbol).build().get_params())

    async def get_price_change_stats_ticker(self, symbol: str):
        """
        Get the 24 hour rolling window price change statistics.

        :param symbol: The symbol of the pair
        :type symbol: string
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element dictionary representing the response

            .. code-block::
            
                {
                    "symbol": "BNBBTC",
                    "priceChange": "-94.99999800",
                    "priceChangePercent": "-95.960",
                    "weightedAvgPrice": "0.29628482",
                    "prevClosePrice": "0.10002000",
                    "lastPrice": "4.00000200",
                    "lastQty": "200.00000000",
                    "bidPrice": "4.00000000",
                    "askPrice": "4.00000200",
                    "openPrice": "99.00000000",
                    "highPrice": "100.00000000",
                    "lowPrice": "0.10000000",
                    "volume": "8913.30000000",
                    "quoteVolume": "15.30000000",
                    "openTime": 1499783499040,
                    "closeTime": 1499869899040,
                    "firstId": 28385,   // First tradeId
                    "lastId": 28460,    // Last tradeId
                    "count": 76         // Trade count
                }
        """          
        return await self._get('ticker/24hr', 
            RequestBuilder().with_symbol(symbol).build().get_params())

    async def get_symbol_price_ticker(self, symbol: str):
        """
        Get the latest price for a symbol or symbols

        :param symbol: The symbol of the pair
        :type symbol: string
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element dictionary representing the response

            .. code-block::
            
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                }
        """             
        return await self._get('ticker/price', 
            RequestBuilder().with_symbol(symbol).build().get_params())

    async def get_symbol_order_book_ticker(self, symbol: str):
        """
        Get the best price/qty on the order book for a symbol or symbols

        :param symbol: The symbol of the pair
        :type symbol: string
        :return: returns a tuple, where the first element is the HTTP 
            response status code and the second element dictionary representing the response

            .. code-block::
            
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                }
        """           
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

