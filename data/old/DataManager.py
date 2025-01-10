import sys
sys.path.append('./')


import requests
import datetime 
import pandas as pd
from constants.bitget_symbols import all_symbols





# class DataManager:
#     intervals = []
#     url = "https://api.bitget.com/api/v2/mix/market/history-index-candles"
#     def __init__():
#         pass

#     def download_candles(self, intervals, url):
#         fetched = []
#         for interval in intervals[:]:
#             params = {
#                 "symbol": "INJUSDT",
#                 "productType": "usdt-futures",
#                 "granularity": "1m",
#                 "endTime": str(int(interval.timestamp()*1000)),
#                 "limit": "200",
#                 # "startTime": str(int(interval.timestamp()*1000))
#             }

#             response = requests.get(url, params=params)

#             data = response.json()['data']
#             fetched.extend(data)

#     def generate_time_intervals(start_datetime, end_datetime=datetime.datetime.now().replace(second=0,microsecond=0) ,interval=200):
    
#         intervals = []
#         current_datetime = start_datetime

#         while current_datetime < end_datetime:

#             intervals.append(current_datetime.replace(second=0,microsecond=0))
#             current_datetime = current_datetime + datetime.timedelta(minutes=interval)

#         return intervals
    

