import os
from loguru import logger
import sys
from datetime import datetime
from config import config

from RedPandaMdProducer import RedPandaMdProducer
from kraken_api.KrakenHistoricalMdSubscriber import KrakenHistoricalMdSubscriber
from kraken_api.KrakenRealtimeMdSubscriber import KrakenRealtimeMdSubscriber

if __name__ == "__main__":

    logger.remove()
    logger.add(sys.stdout,
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
               level="INFO")

    broker_address = os.getenv('BROKER_ADDRESS', 'localhost:19092')
    tickers = config.tickers
    mode = config.mode

    topic_name = config.topic_name
    if mode == 'historical':
        from_dt_str = config.from_time

        to_dt_str = config.to_time

        logger.info(f"Fetching historical data for {tickers} from {from_dt_str} to {to_dt_str}")

        subscriber = KrakenHistoricalMdSubscriber(tickers=tickers,
                                                  from_dt_str=from_dt_str,
                                                  to_dt_str=to_dt_str,
                                                  broker_address=broker_address,
                                                  topic_name=topic_name,
                                                  trace=True)
        subscriber.run_forever()

    elif mode == 'realtime':
        logger.info(f"Fetching realtime data for {tickers}")
        producer = RedPandaMdProducer(broker_address=broker_address, topic_name=topic_name)
        subscriber = KrakenRealtimeMdSubscriber(tickers=tickers,
                                                on_trade_message=producer.on_trade,
                                                trace=True)
        subscriber.run_forever()

    else:
        logger.error(f"Invalid mode: {mode}")
        sys.exit(1)
