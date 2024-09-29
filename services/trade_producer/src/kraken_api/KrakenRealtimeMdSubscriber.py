import websocket
import json
from datetime import datetime
from loguru import logger
import os

class KrakenRealtimeMdSubscriber:

    def __init__(self, tickers, on_trade_message=None, trace=False):
        self.tickers = tickers
        self.on_trade_message = on_trade_message
        self.trace = trace

        # Create the trade subscription message with the tickers
        self.trade_subscription_message = {
            "method": "subscribe",
            "params": {
                "channel": "trade",
                "symbol": tickers
            }
        }

        self.ws = websocket.WebSocketApp("wss://ws.kraken.com/v2",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def run_forever(self) -> bool:
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

        if channel == 'trade':
            for item in data_list:
                symbol = item['symbol']
                side = item['side']
                price = item['price']
                qty = item['qty']

                # Convert timestamp to epoch
                timestamp_str = item['timestamp']
                timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                time_dbl = timestamp_dt.timestamp()
                epoch_time_ms = int(time_dbl * 1e3)

                if self.trace:
                    print(f"Trade - Symbol: {symbol}, Price: {price}, Qty: {qty}, Side: {side}, TimeMs: {epoch_time_ms}")

                if self.on_trade_message is not None:
                    self.on_trade_message(symbol, epoch_time_ms, price, qty, side)

    def on_error(self, ws, error):
        logger.error(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info("### closed ###")

    def on_open(self, ws):
        logger.info("Opened connection..")

        logger.info("Subscribing to Trades")
        ws.send(json.dumps(self.trade_subscription_message))


if __name__ == "__main__":

    # print python path
    print(os.environ['PYTHONPATH'])

    tickers = ["ETH/USD", "BTC/USD"]

    def on_trade(symbol, timestamp_ms, price, qty, side):
        print(f"Symbol: {symbol}, TimeMs:{timestamp_ms}, Price: {price}, Qty: {qty}, Side: {side}")

    subscriber = KrakenRealtimeMdSubscriber(tickers, on_trade_message=on_trade, trace=True)
    subscriber.run_forever()

    print("Done")
