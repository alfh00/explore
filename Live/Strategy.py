import threading
import copy
import pandas as pd
from thread_base import ThreadBase
from apis.ApiClient import BitgetClient


class Strategy(ThreadBase):

    def __init__(self, shared_prices, price_lock: threading.Lock, price_events, shared_candles, candle_lock, candle_events, api, logname, pair, settings):
        super().__init__(shared_prices, price_lock, price_events,shared_candles, candle_lock, candle_events, logname, api=api)
        self.pair = pair
        self.settings = settings
        self.api: BitgetClient = api
        self.df = None

    def update_df(self, candle):
        if self.df is None:
            self.df = self.api.get_last_historical(self.pair, self.settings.granularity, limit=100)
            
        else:
            new_row = pd.DataFrame([candle]).set_index('time')
            self.df = pd.concat([self.df, new_row], ignore_index=False)
        self.log_message(f'DF updated :\n {self.df.tail(2)}')
    
    def process_candle(self): 
        try:
            self.candle_lock.acquire()
            candle = copy.deepcopy(self.shared_candles[self.pair])
            self.update_df(candle)
            self.log_message(f'Candle received : {candle}')
        except Exception as e:
            self.log_message(f'CRASH : {e}', error=True)
        finally:
            self.candle_lock.release()

    def run(self):
        while True:
            self.candle_events[self.pair].wait()
            self.process_candle()
            self.candle_events[self.pair].clear()
        