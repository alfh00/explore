import ccxt
import time
import pandas as pd
import numpy as np
from time import sleep
import datetime


exchange = ccxt.bitget()

class Ticker:
    def __init__(self, symbol, tf):
        self.symbol = symbol
        self.exchange = ccxt.bitget()
        self.tf = tf

    def generate_time_intervals(self, start_datetime, end_datetime=datetime.datetime.now() ,interval=1000):
        intervals = []
        current_datetime = start_datetime
        while current_datetime < end_datetime:
            intervals.append(current_datetime)
            current_datetime = current_datetime + datetime.timedelta(minutes=1000)
        return intervals
    
    def fetch_candles(self, since):
        try:
            candles = exchange.fetch_ohlcv(self.symbol, self.tf, since, limit=1000)
            return candles
        except ccxt.BaseError as e:
            print(f"Erreur lors du téléchargement des bougies : {str(e)}")
            return []
    
    def to_dataframe(self, data):
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df.drop('timestamp', axis=1, inplace=True)
        df.set_index('date', inplace=True)
        return df