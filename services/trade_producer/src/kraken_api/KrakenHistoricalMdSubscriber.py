import websocket
import json
from datetime import datetime
from loguru import logger
import requests
from concurrent.futures import ThreadPoolExecutor

from kraken_api.KrakenHistoricalMdApi import KrakenHistoricalMdApi
from RedPandaMdProducer import RedPandaMdProducer

class KrakenHistoricalMdSubscriber:

    def __init__(self, tickers, from_dt_str, to_dt_str, broker_address,
                 topic_name, max_workers = 5,
                 on_trade_message=None, trace=False, enable_threading=False):

        self.subscribers = []

        for ticker in tickers:
            producer = RedPandaMdProducer(broker_address=broker_address, topic_name=topic_name)
            self.subscribers.append(KrakenHistoricalMdApi(ticker,
                                                          from_dt_str=from_dt_str,
                                                          to_dt_str=to_dt_str,
                                                          on_trade_message=producer.on_trade,
                                                          trace=trace))
        self.max_workers = max_workers
        self.enable_threading = enable_threading

    def run_forever(self):

        if self.enable_threading:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(subscriber.run_forever) for subscriber in self.subscribers]

                for future in futures:
                    future.result()
        else:
            for subscriber in self.subscribers:
                subscriber.run_forever()

if __name__ == "__main__":

    ticker = "ETH/USD"
    from_dt = "2024-09-20 00:00:00"
    to_dt = "2024-09-21 00:00:00"

    subscriber = KrakenHistoricalMdSubscriber(ticker, from_dt, to_dt, on_trade_message=None, trace=True)
    subscriber.run_forever()

    print("Done")
