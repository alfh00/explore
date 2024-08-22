import ccxt.async_support as ccxt

CCXT_EXCHANGES = {
        "binance": {
            "ccxt_object": ccxt.binance(config={'enableRateLimit': True}),
            "limit_size_request": 1000
        },
        "binanceusdm": {
            "ccxt_object": ccxt.binanceusdm(config={'enableRateLimit': True}),
            "limit_size_request": 1000
        },
        "kucoin": {
            "ccxt_object": ccxt.kucoin(config={'enableRateLimit': True}),
            "limit_size_request": 200
        },
        "kucoinfutures": {
            "ccxt_object": ccxt.kucoinfutures(config={'enableRateLimit': True}),
            "limit_size_request": 200
        },
        "okx": {
            "ccxt_object": ccxt.okx(config={'enableRateLimit': True}),
            "limit_size_request": 100
        },
        "bitget": {
            "ccxt_object": ccxt.bitget(config={'enableRateLimit': True}),
            "limit_size_request": 200
        },
        "bybit": {
            "ccxt_object": ccxt.bybit(config={'enableRateLimit': True}),
            "limit_size_request": 1000
        }
    }