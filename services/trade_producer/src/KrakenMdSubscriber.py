import websocket
import json
from datetime import datetime
from loguru import logger

class KrakenMdSubscriber:

    def __init__(self, subscribe_trade=True, subscribe_l1=True, on_l1_message=None, on_trade_message=None, trace=False):
        self.subscribe_trade = subscribe_trade
        self.subscribe_l1 = subscribe_l1
        self.on_l1_message = on_l1_message
        self.on_trade_message = on_trade_message
        self.trace = trace

        self.trade_subscription_message = {
            "method": "subscribe",
            "params": {
                "channel": "trade",
                "symbol": [
                    "ETH/USD"
                ]
            }
        }

        self.l1_subscription_message = {
            "method": "subscribe",
            "params": {
                "channel": "ticker",
                "symbol": [
                    "ETH/USD"
                ],
                "event_trigger": "bbo",
            }
        }

        self.ws = websocket.WebSocketApp("wss://ws.kraken.com/v2",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def run_forever(self):
        self.ws.run_forever()

    def on_message(self, ws, message):
       
        if 'heartbeat' in message:
            return

        if "subscribe" in message:
            return

        if "status" in message:
            return

        data = json.loads(message)
        channel = data['channel']
        data_list = data['data']
       
        if channel == 'ticker':
            for item in data_list:
                symbol = item['symbol']
                bid = item['bid']
                ask = item['ask']
                bid_qty = item['bid_qty']
                ask_qty = item['ask_qty']

                if self.trace:  
                    print(f"L1 - Symbol: {symbol}, Bid: {bid}, Ask: {ask}, Bid Qty: {bid_qty}, Ask Qty: {ask_qty}")

                if self.on_l1_message is not None:
                    self.on_l1_message(symbol, bid, ask, bid_qty, ask_qty)

        elif channel == 'trade':
            for item in data_list:
                symbol = item['symbol']
                side = item['side']
                price = item['price']
                qty = item['qty']
        
                # Convert timestamp to epoch
                timestamp_str = item['timestamp']
                timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                epoch_time = int(timestamp_dt.timestamp())

                if self.trace:
                    print(f"Trade - Symbol: {symbol}, Price: {price}, Qty: {qty}, Side: {side}, Timestamp: {epoch_time}")

                if self.on_trade_message is not None:
                    self.on_trade_message(symbol, price, qty, side)

    def on_error(self, ws, error):
        logger.error(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info("### closed ###")

    def on_open(self, ws):
        logger.info("Opened connection..")
    
        if self.subscribe_l1:
            logger.info("Subscribing to L1")
            ws.send(json.dumps(self.l1_subscription_message))

        if self.subscribe_trade:
            logger.info("Subscribing to Trades")
            ws.send(json.dumps(self.trade_subscription_message))

        
if __name__ == "__main__":
    subscriber = KrakenMdSubscriber(subscribe_trade=True, subscribe_l1=True, trace=True)
    subscriber.run_forever()

    print("Done")
