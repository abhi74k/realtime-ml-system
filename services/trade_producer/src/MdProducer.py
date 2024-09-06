from RedPandaMdProducer import RedPandaMdProducer
from KrakenMdSubscriber import KrakenMdSubscriber
import os

if __name__ == "__main__":

    broker_address = os.getenv('BROKER_ADDRESS', 'localhost:19092')
    producer = RedPandaMdProducer(broker_address=broker_address, topic_name='marketdata')
    subscriber = KrakenMdSubscriber(subscribe_trade=True,
                                    subscribe_l1=True,
                                    on_l1_message=producer.on_nbbo, 
                                    on_trade_message=producer.on_trade)
    subscriber.run_forever()


