from pybitget.stream import BitgetWsClient, SubscribeReq, handel_error

from pybitget.enums import *
from pybitget import logger
import json

from Live.ApiClient import BitgetClient

SYMBOL = 'ARBUSDT'
bitget = BitgetClient()

# f = open(
#     "./secret.json",
# )
# secret = json.load(f)
# f.close()

# api_key = "your-api-key"
# api_secret = "your-secret-key"
# api_passphrase = "your-api-passphrase"

dist =0.003
sl_pct=0.01
tp_pct=0.06
trailing_sl_trigger_pct=0.001
trailing_sl_pct=0.001

def get_last_canles():
    pass

def find_last_high_low():
    pass

def place_trigger_order():
    pass

def trail_stop():
    pass

def on_message(message):
    data = json.loads(message)
    if data['action'] == 'snapshot':
        last_candlestick = data['data']
        
        logger.info(last_candlestick)
    elif data['action'] == 'update':
        logger.info(data['data'])




if __name__ == '__main__':
    # Un-auth subscribe
    client = BitgetWsClient() \
        .error_listener(handel_error) \
        .build()

    # Auth subscribe
    # client = BitgetWsClient(api_key=api_key,
    #                         api_secret=api_secret,
    #                         passphrase=api_passphrase,
    #                         verbose=True) \
    #     .error_listener(handel_error) \
    #     .build()

    # multi subscribe  - Public Channels
    # channels = [SubscribeReq("mc", "ticker", "INJUSDT"), SubscribeReq("SP", "candle15m", "BTCUSDT")]
    # client.subscribe(channels, on_message)

    # single subscribe -     # multi subscribe  Public Channels
    channels = [SubscribeReq("mc", "ticker", SYMBOL)]
    client.subscribe(channels, on_message)


    # single subscribe - Order Channel - Private Channels
    # channels = [SubscribeReq(WS_CHANNEL_INSTTYPE, WS_PRIVATE_ORDERS_CHANNEL, WS_CHANNEL_INSTID)]
    # client.subscribe(channels, on_message)
