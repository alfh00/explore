from datetime import datetime as dt
from apis.bitget_client import BitgetClient

class OrderManager:
    def __init__(self, symbol, api: BitgetClient):
        """
        Initialize the OrderManager with an API session.
        :param api: An API Client session object that holds market information and provides order execution.
        """
        self.api = api
        self.symbol = symbol
        self.contract = self.get_instrument_contract()

    def oid(self):
        pass

    def get_instrument_contract(self):
        contract = self.api.contracts(dict(symbol=self.symbol, productType='USDT-FUTURES'))
        return contract['data'][0]

    def place_trigger_order(self, size, side, order_type, price, oid='001'):
        
        params = {
            "planType": "normal_plan",                   # 'normal_plan' | 'track_plan'
            "symbol": self.symbol,
            "productType": "USDT-FUTURES",
            "marginMode": "isolated",
            "marginCoin": "USDT",
            "size": size,
            "price": price,             
            "triggerPrice": price,       
            "triggerType": "mark_price",    
            "side": side,                                # 'buy'   | 'sell'
            "tradeSide": 'open',                         # 'open'  | 'close'
            "orderType": order_type,                     # 'limit' | 'market'
            "clientOid": oid,
        }
        # {
        #     "planType": "normal_plan",
        #     "symbol": "BTCUSDT",
        #     "productType": "USDT-FUTURES",
        #     "marginMode": "isolated",
        #     "marginCoin": "USDT",
        #     "size": "0.01",
        #     "price": "24000",
        #     "triggerPrice": "24100",
        #     "triggerType": "mark_price",
        #     "side": "buy",
        #     "tradeSide": "open",
        #     "orderType": "limit",
        #     "clientOid": "unique_client_id_12345",
        #     "reduceOnly": "NO",
        #     "stopSurplusTriggerPrice": "25000",
        #     "stopSurplusTriggerType": "mark_price",
        #     "stopLossTriggerPrice": "23000",
        #     "stopLossTriggerType": "mark_price"
        # }

        try:
            # Place the order through the session (API)
            response = self.api.placePlanOrder(params)
            return response
        except Exception as e:
            return f"Failed to place order: {e}"

    def trail_stop(self, current_position, price, trailing_sl_trigger_pct, trailing_sl_pct):
        """
        Adjust the trailing stop loss based on price movement for crypto.
        

        """
        sl = current_position['sl']  # Existing stop loss
        entry_price = current_position['openPriceAvg']  # Entry price of the position

        # Trailing stop for BUY position
        if current_position['holdSide'] == 'long':
            bid = price['bid']  # Use the close price as bid price for simplicity
            if (bid - entry_price) > (trailing_sl_trigger_pct * entry_price):  # Trigger condition
                new_sl = bid - (trailing_sl_pct * entry_price)  # Calculate new stop loss
                if new_sl > sl:  # Only update if the new stop loss is higher (to protect profits)
                    current_position['sl'] = new_sl  # Update the stop loss

        # Trailing stop for SELL position
        elif current_position['side'] == 'short':
            ask = price['ask']  # Use the close price as ask price for simplicity
            if (entry_price - ask) > (trailing_sl_trigger_pct * entry_price):  # Trigger condition
                new_sl = ask + (trailing_sl_pct * entry_price)  # Calculate new stop loss
                if new_sl < sl:  # Only update if the new stop loss is lower (to protect profits)
                    current_position['sl'] = new_sl  # Update the stop loss

        return current_position

    def get_all_positions(self, prodcut_type, margin_coin):
        params = {
            "productType": "USDT-FUTURES",
            "marginCoin": "USDT",
        }

        try:
            response = self.api.allPosition(params)
            positions = response['data']
            return positions
        except Exception as e:
            return f"Failed to get all position: {e}"
    
    def get_order_detail(self, symbol, oid):
        params = {
            "symbol": symbol,
            "productType": "USDT-FUTURES",
            "orderId": "",
            "clientOid": oid,
        }

        try:
            response = self.api.detail(params)
            order_detail = response['data']
            return order_detail
        except Exception as e:
            return f"Failed to get order detail: {e}"


    def get_min_order_amount(self, symbol):
        """
        Retrieve the minimum allowable order size for a specific trading pair.

        """
        return self._session.markets_by_id[symbol]["info"]["minProvideSize"]

    def convert_amount_to_precision(self, symbol, amount):
        """
        Format the order amount to the required precision for the given symbol.
        :param symbol: Trading pair symbol, e.g., 'BTCUSDT'.
        :param amount: Desired order amount.
        :return: Amount formatted to the required precision.
        """
        return self._session.amount_to_precision(symbol, amount)

    def convert_price_to_precision(self, symbol, price):
        """
        Format the order price to the required precision for the given symbol.
        :param symbol: Trading pair symbol, e.g., 'BTCUSDT'.
        :param price: Desired order price.
        :return: Price formatted to the required precision.
        """
        return self._session.price_to_precision(symbol, price)

    def is_valid_order(self, symbol, amount):
        """
        Check if the order amount is valid based on the minimum order size.
        :param symbol: Trading pair symbol, e.g., 'BTCUSDT'.
        :param amount: Desired order amount.
        :return: Boolean indicating if the order amount is valid.
        """
        min_amount = float(self.get_min_order_amount(symbol))
        return amount >= min_amount


# Example usage:
# session = YourAPISession()  # Replace with an initialized API session
# order_manager = OrderManager(session)
# response = order_manager.place_order(symbol="BTCUSDT", side="buy", order_type="limit", amount=0.01, price=35000)
# print(response)
