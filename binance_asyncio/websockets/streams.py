from typing import Callable, Tuple
from abc import ABC, abstractmethod
import websockets
import json

class BaseStream(ABC):
    uri = "wss://stream.binance.com:9443/ws"
    last_id = 0

    def __init__(self) -> None:
        self.parameters = {}
        self.active = True
        self.active_id = None
        self.socket_reference = None

    async def start(self,  handler: Callable, keep_alive=False):
        self.active_id = BaseStream.last_id = BaseStream.last_id + 1
        if not keep_alive:
            await self._start(handler)
        else:
            while self.active:
                try:
                    await self._start(handler)
                except:
                    continue

    async def _start(self,  handler: Callable):
        async with websockets.connect(BaseStream.uri) as websocket:
            self.socket_reference = websocket
            request = await self._get_request('SUBSCRIBE')
            await websocket.send(request)
            await websocket.recv()
            async for message in websocket:
                await handler(message)

    @abstractmethod
    async def get_stream_identifier(self) -> str:
        pass

    async def subscribe(self, symbol:str) -> None:
        await self._subscribe(symbol)

    async def _subscribe(self, *args:str):
        await self._add_parameter(args)
        if self.socket_reference is not None:
            await self.socket_reference.send(await self._get_request('SUBSCRIBE'))


    async def _get_request(self, type:str):
        parameters = list(self.parameters.keys())
        return json.dumps({
                "method": type,
                "params": parameters,
                "id": self.active_id
                })

    async def _add_parameter(self, args):
        parameter = (await self.get_stream_identifier()).format(*args)
        self.parameters[parameter] = None

class AggregateTradeStream(BaseStream):
    async def get_stream_identifier(self) -> str:
        return "{}@aggTrade"

class TradeStream(BaseStream): 
    async def get_stream_identifier(self) -> str:
        return "{}@trade"

class TickerStream(BaseStream):
    async def get_stream_identifier(self) -> str:
        return "{}@ticker"

class AllMarketTickerStream(BaseStream):
    async def get_stream_identifier(self) -> str:
        return "!ticker@arr"

class MiniTickerStream(BaseStream):    
    async def get_stream_identifier(self) -> str:
        return "{}@miniTicker"

class AllMarketsMiniTickerStream(BaseStream):
    async def get_stream_identifier(self) -> str:
        return "!miniTicker@arr"

class KlineStream(BaseStream):
    async def subscribe(self, symbol:str, interval:str) -> None:
        arguments = [symbol, interval]
        await super()._subscribe(*arguments)

    async def get_stream_identifier(self) -> str:
        return "{}@kline_{}"

class SymbolBookTickerStream(BaseStream):
    async def get_stream_identifier(self) -> str:
        return "{}@bookTicker"

class AllBookTickerStream(BaseStream):
    async def get_stream_identifier(self) -> str:
        return "!bookTicker"

class PartialBookDepthStream(BaseStream):
    async def subscribe(self, symbol:str, levels:str, more_updates:bool=False) -> None:
        arguments = [symbol, levels, "" if not more_updates else "@100ms"]
        await super()._subscribe(*arguments)

    async def get_stream_identifier(self) -> str:
        return "{}@depth{}{}"

class DiffDepthStream(BaseStream):
    async def subscribe(self, symbol:str, more_updates:bool=False) -> None:
        arguments = [symbol, "" if not more_updates else "@100ms"]
        await super()._subscribe(*arguments)
    async def get_stream_identifier(self) -> str:
        return "{}@depth{}"