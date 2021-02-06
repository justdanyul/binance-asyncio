# Welcome to binance-asyncio

This is an unofficial wrapper for the Binance API, as per the license, its provided with no guarantee, so use it at your own risk.

## Quick start

Install with  
``pip install binance-asyncio``

Have a look at the `examples` directory, to get you started (until I publish some docs)

## Current status

This is very much work-in-process, I made it for some personal projects, where I needed to be able to interact with binance in an asyncio
context. And its been working well for me, so I thought I'd share it. 

### Status of documentation
Currently, non-existing. I'll get the sphinx docs up and running on read the docs shortly.

Until then please just refer to the `examples` directory.

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
- [ ] Individual Symbol Book Ticker Streams
- [ ] All Book Tickers Stream
- [ ] Partial Book Depth Streams
- [ ] Diff. Depth Stream