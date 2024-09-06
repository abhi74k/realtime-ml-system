from RedPandaMdProducer import RedPandaMdProducer
from KrakenMdSubscriber import KrakenMdSubscriber


if __name__ == "__main__":

    producer = RedPandaMdProducer(broker_address='localhost:19092', topic_name='marketdata')
    subscriber = KrakenMdSubscriber(subscribe_trade=True,
                                    subscribe_l1=True,
                                    on_l1_message=producer.on_nbbo, 
                                    on_trade_message=producer.on_trade)
    subscriber.run_forever()


