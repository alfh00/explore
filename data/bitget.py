import os
import requests
import datetime 
import pandas as pd
import json
import pytz
import time

import concurrent.futures
import threading

request_limit = 20  # Maximum number of requests per second
semaphore = threading.Semaphore(request_limit)

# declare timeframes
# timeframes = ['1W', '1D', '4H', '1H', '30m', '15m', '5m', '1m' ]
timeframes = ['1H']
start_datetime = '2020-01-01 00:00:00'

# load all instruments
# with open('constants/bitget_symbols.json', 'r') as file:
#     data = json.load(file)
# instruments = data.keys()
# print(len(instruments))
# instruments = ['INJUSDT', 'FETUSDT', 'ARBUSDT', 'SEIUSDT']
instruments = ['BTCUSDT']

# generate time intervals
def generate_time_intervals(start_datetime, end_datetime=datetime.datetime.now().replace(second=0, microsecond=0), timeframe='1D', range=200):
    intervals = []
    current_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone('Europe/Paris'))
    end_datetime = end_datetime.replace(tzinfo=pytz.timezone('Europe/Paris'))

    # Define the size of the intervals for each timeframe
    timeframe_intervals = {
        '1W': datetime.timedelta(weeks=1*12),
        '1m': datetime.timedelta(minutes=1*range),
        '5m': datetime.timedelta(minutes=5*range),
        '15m': datetime.timedelta(minutes=15*range),
        '30m': datetime.timedelta(minutes=30*range),
        '1H': datetime.timedelta(hours=1*range),
        '4H': datetime.timedelta(hours=4*range),
        '1D': datetime.timedelta(days=1*90),
    }

    # Get the size of the intervals for the specified timeframe
    interval = timeframe_intervals[timeframe]

    # Generate the intervals
    while current_datetime < end_datetime:
        intervals.append(current_datetime.replace(second=0, microsecond=0))
        current_datetime = current_datetime + interval
    
    return intervals

def fetch_data(symbol, granularity, start_time, end_time, product='usdt-futures'):

    start_time = int(start_time.timestamp()) * 1000
    end_time = int(end_time.timestamp()) * 1000

    # print(start_time)
    # print(end_time)

    url = f"https://api.bitget.com/api/v2/mix/market/history-mark-candles"
    # url = f"https://api.bitget.com/api/v2/mix/market/candles?symbol={symbol}&granularity={granularity}&limit={limit}&productType={product_type}"
    
    params = {
                    "symbol": f"{symbol}",
                    "productType": product,
                    "granularity": f"{granularity}",
                    "limit": "200",
                    "startTime": start_time,
                    "endTime": end_time
                }

    with semaphore:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Release the semaphore after the request
        time.sleep(1 / request_limit)  # Sleep to maintain the request rate
        # print(data)
        return data

def to_dataframe(data):
    # print(data)
    df = pd.DataFrame(data, columns=['datetime', 'open', 'high', 'low', 'close', 'volume', 'quote_volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms', origin='unix')
    df.set_index('datetime', inplace=True)
    return df


for timeframe in timeframes:
    # Check if the directory exists
    if not os.path.exists(f'./DB/{timeframe}'):
        # Create the directory
        os.mkdir(f'./DB/{timeframe}')
    
    intervals = generate_time_intervals(start_datetime, timeframe=timeframe)
    
    for symbol in instruments:
        print(f'start fetching... {symbol}__{timeframe}')
        data = []
        for i in range(0, len(intervals)-1):
            # print(intervals[i])
            # print(intervals[i+1])
            fetched = fetch_data(symbol, timeframe, intervals[i], intervals[i+1])
            # print('fetched______________',fetched)
            if fetched :
                data.extend(fetched['data'])
        # print(data)
        df = to_dataframe(data)

        df.to_csv(f'./DB/{timeframe}/{symbol}_{timeframe}.csv')

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = list(executor.map(lambda interval: fetch_data(interval, time_frame), intervals))
