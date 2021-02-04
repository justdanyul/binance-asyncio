import time
from typing import Dict
import dateparser

class Request:
    def __init__(self) -> None:
        self.parameters:dict = dict()

    def add_param(self, name, value) -> None:
        self.parameters[name] = value
    
    def add_parameters(self, param_dict: Dict) -> None:
        for name, value in param_dict.items():
            self.parameters[name] = value

    def get_params(self) -> dict:
        empty_params = [key for key, value in self.parameters.items() if value is None]
        for key in empty_params:
            del self.parameters[key]
        return self.parameters


class RequestBuilder:
    def __init__(self) -> None:
        self.request = Request()
    
    def with_symbol(self, symbol: str):
        self.request.add_param('symbol', symbol.upper())
        return self

    def with_start_time(self, time:str):
        self.request.add_param('startTime', self.__parse_time(time))
        return self

    def with_end_time(self, time:str):
        self.request.add_param('endTime', self.__parse_time(time))
        return self

    def with_limit(self, limit:int):
        self.request.add_param('limit', limit)
        return self
    
    def with_from_id(self, from_id:str):
        self.request.add_param('from_id', from_id)
        return self

    def with_interval(self, interval:str):
        self.request.add_param('interval', interval)
        return self

    def with_timestamp(self):
        timestamp = int(round(time.time() * 1000))
        self.request.add_param('timestamp', timestamp)
        return self

    def build(self):
        return self.request

    def __parse_time(self, time:str):
        if time is None or time == "":
            raise Exception("Invalid time format")
        return int(dateparser.parse(time).timestamp() * 1000)