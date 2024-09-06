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

    def on_nbbo(self, symbol, bid, ask, bid_qty, ask_qty):

        message = {
            "symbol": symbol,
            "bid": bid,
            "ask": ask,
            "bid_qty": bid_qty,
            "ask_qty": ask_qty
        }
        
        self.__publish(message)

    def on_trade(self, symbol, price, qty, side):

        message = {
            "symbol": symbol,
            "price": price,
            "qty": qty,
            "side": side
        }

        self.__publish(message)

    def __publish(self, event):
        message = self.topic.serialize(key=event['symbol'], value=event)
        self.producer.produce(topic=self.topic.name, key=message.key, value=message.value)

    def __del__(self):
        if self.producer is not None:
            self.producer.close()