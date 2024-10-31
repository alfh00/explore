from apis.PriceStreamer import PriceStreamer
from apis.ApiClient import BitgetClient
from logger import Logger
from models.trade_settings import TradeSettings
from models.api_secrets import ApiSecrets
from PriceProcessor import PriceProcessor
from Strategy import Strategy
import json
import time
import threading
from queue import Queue

class TraderBot():
    ERROR_LOG = 'error'
    MAIN_LOG = 'main'
    GRANULARITY = '1m'
    ACCOUNT= 'bitget1'
    SLEEP = 10

    def __init__(self):
       # Load settings and secrets
        self.load_settings()
        self.load_secrets()
        self.setup_logs()

        
        self.shared_prices = {symbol: None for symbol in self.trade_settings.keys()}
        self.price_lock = threading.Lock() 
        self.price_events = {symbol: threading.Event() for symbol in self.trade_settings.keys()}
        
        self.shared_candles = {symbol: None for symbol in self.trade_settings.keys()}
        self.candle_lock = threading.Lock()  
        self.candle_events = {symbol: threading.Event() for symbol in self.trade_settings.keys()}

        # work_queue = Queue()

        threads = []


        # Initialize API client, PriceStreamer and DataManager
        self.api = BitgetClient(self.api_secrets.public_api, self.api_secrets.secret_api, self.api_secrets.password)
        
        self.price_streamer = PriceStreamer(self.shared_prices, self.price_lock, self.price_events, self.candle_events)
        for pair, pair_setting in self.trade_settings.items():
            price_processor_t = PriceProcessor(self.shared_prices, 
                                               self.price_lock, 
                                               self.price_events, 
                                               self.shared_candles,
                                               self.candle_lock, 
                                               self.candle_events,
                                               f'PriceProcess_{pair}', 
                                               pair, 
                                               pair_setting.granularity
                                               )
            price_processor_t.daemon = True
            threads.append(price_processor_t)
            price_processor_t.start()

        for pair, pair_setting in self.trade_settings.items():
            strategy_processor_t = Strategy(self.shared_prices, 
                                               self.price_lock, 
                                               self.price_events, 
                                               self.shared_candles,
                                               self.candle_lock, 
                                               self.candle_events,
                                               self.api,
                                               f'StrategyProcess_{pair}', 
                                               pair, 
                                               pair_setting
                                               )
            strategy_processor_t.daemon = True
            threads.append(strategy_processor_t)
            strategy_processor_t.start()


    def setup_logs(self):
        self.logs = {}
        for k in self.trade_settings.keys():
            self.logs[k] = Logger(k)
            self.log_message(f'{self.trade_settings[k]}', k)
        self.logs[TraderBot.ERROR_LOG] = Logger(TraderBot.ERROR_LOG)
        self.logs[TraderBot.MAIN_LOG] = Logger(TraderBot.MAIN_LOG)
        self.log_to_main(f'TraderBot started with {TradeSettings.settings_to_str(self.trade_settings)}')
    
        
    def log_message(self, msg, key):
        self.logs[key].logger.debug(msg)

    def log_to_main(self, msg):
        self.log_message(msg, TraderBot.MAIN_LOG)

    def log_to_error(self, msg):
        self.log_message(msg, TraderBot.ERROR_LOG)

    def load_settings(self):
        with open('./Live2/setting.json', 'r') as f:
            data = json.loads(f.read())
            self.trade_settings = {symbol: TradeSettings(settings) for symbol, settings in data.items()}
            print(self.trade_settings)
    
    def load_secrets(self):
        with open('./Live2/secrets.json', 'r') as f:
            data = json.loads(f.read())
            data = data[self.ACCOUNT]
            self.api_secrets = ApiSecrets(data) 


    def run(self):
        pass





if __name__ == '__main__':
    b = TraderBot()
