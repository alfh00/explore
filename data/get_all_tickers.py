import requests
import json

url = "https://api.bitget.com/api/v2/mix/market/tickers?productType=USDT-FUTURES"

def get_all_tickers(url):
    bitget_symbols = {}

    response = requests.get(url)
    data = response.json()['data']

    for symbol in data:
        bitget_symbols[symbol['symbol']]= {'fundingRate':symbol['fundingRate']}

    with open('./DB/bitget_symbols.json', 'w') as f:
        f.write(json.dumps(bitget_symbols, indent=2))
    

get_all_tickers(url)