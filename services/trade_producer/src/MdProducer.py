from RedPandaMdProducer import RedPandaMdProducer
from KrakenMdSubscriber import KrakenMdSubscriber
import os
from loguru import logger
import sys
from datetime import datetime

if __name__ == "__main__":

    logger.remove()
    logger.add(sys.stdout, 
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
               level="INFO")

    broker_address = os.getenv('BROKER_ADDRESS', 'localhost:19092')
    producer = RedPandaMdProducer(broker_address=broker_address, topic_name='marketdata')
    subscriber = KrakenMdSubscriber(subscribe_trade=True,
                                    subscribe_l1=True,
                                    on_l1_message=producer.on_nbbo, 
                                    on_trade_message=producer.on_trade)
    subscriber.run_forever()


