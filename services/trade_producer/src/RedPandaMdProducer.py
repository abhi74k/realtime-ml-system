# Simple quix stream producter to send trades to the quix stream in a loop. The loop should sleep 1 second between each iteration.

import quixstreams as qx
import time

from quixstreams import Application

class RedPandaMdProducer:

    def __init__(self, broker_address, topic_name) -> None:

        self.broker_address = broker_address
        self.app = Application(broker_address=self.broker_address)
        self.topic = self.app.topic(name=topic_name, value_serializer='json')
        self.producer = self.app.get_producer()

    def on_nbbo(self, symbol, timestamp_ms, bid, ask, bid_qty, ask_qty):

        message = {
            "symbol": symbol,
            "bid": bid,
            "ask": ask,
            "bid_qty": bid_qty,
            "ask_qty": ask_qty
        }

        self.__publish(message)

    def on_trade(self, symbol, time_ms, price, qty, side):

        message = {
            "symbol": symbol,
            "price": price,
            "qty": qty,
            "side": side,
            "timestamp_ms": time_ms
        }

        self.__publish(message)

    def __publish(self, event):
        message = self.topic.serialize(key=event['symbol'], value=event, timestamp_ms=event['timestamp_ms'])
        self.producer.produce(topic=self.topic.name, key=message.key, value=message.value, timestamp=event['timestamp_ms'])

    def __del__(self):
        if self.producer is not None:
            self.producer.__exit__(None, None, None)