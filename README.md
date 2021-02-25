# Welcome to binance-asyncio

[![Documentation Status](https://readthedocs.org/projects/binance-asyncio/badge/?version=latest)](https://binance-asyncio.readthedocs.io/en/latest/?badge=latest)

This is an unofficial wrapper for the Binance API, as per the license, its provided with no guarantee, so use it at your own risk.

## Quick start

Install with  

```
pip install binance-asyncio
```

And have a look at the `examples` directory, to get you started

## Current status

This is very much work-in-process, I made it for some personal projects, where I needed to be able to interact with binance in an asyncio
context. And its been working well for me, so I thought I'd share it. 

### Status of documentation
I got a very early version of the documentation ready here at: [binance-asyncio.readthedocs.io](https://binance-asyncio.readthedocs.io)


Its still a WIP, but should prove helpful regardless. Also, as mentioned, you can also look in the `examples` directory to get started.

### Coverage of API

- [x] General endpoints (full coverage)
- [x] Market Data endpoints (full coverage)
- [ ] Account endpoints (order and test order implemented)

### Stream coverage
- [x] Aggregate Trade Streams
- [x] Trade Streams
- [x] Kline/Candlestick Streams
- [x] Individual Symbol Mini Ticker Stream
- [x] All Market Mini Tickers Stream
- [x] Individual Symbol Ticker Streams
- [x] All Market Tickers Stream
- [x] Individual Symbol Book Ticker Streams
- [x] All Book Tickers Stream
- [x] Partial Book Depth Streams
- [x] Diff. Depth Stream