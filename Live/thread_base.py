import threading
from logger import Logger

class ThreadBase(threading.Thread):

    def __init__(self, shared_prices, price_lock: threading.Lock, price_events, shared_candles, candle_lock, candle_events, logname, api=None):
        super().__init__()
        self.shared_prices = shared_prices
        self.price_lock = price_lock
        self.price_events = price_events
        self.shared_candles = shared_candles
        self.candle_lock = candle_lock
        self.candle_events = candle_events
        self.api = api or None
        self.log = Logger(logname)

    def log_message(self, msg, error=False):
        if error == True:
            self.log.logger.error(msg)
        else:            
            self.log.logger.debug(msg)