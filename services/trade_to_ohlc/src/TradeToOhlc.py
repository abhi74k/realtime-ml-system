from datetime import timedelta
from quixstreams import Application
from loguru import logger
import os
from config import config
import sys
from datetime import datetime

class TradeToOhlc:
    """
    TradeToOhlc is a class that converts trade data to OHLC data.
    It reads trade data from a Kafka topic, converts it to OHLC data, and writes it to another Kafka topic.
    """
    def __init__(self, broker_address: str, input_topic_name: str, output_topic_name: str, consumer_group:str, window_duration_secs: int = 10):

        self.app = Application(broker_address=broker_address, consumer_group=consumer_group, auto_offset_reset="earliest")

        self.input_topic = self.app.topic(input_topic_name, value_deserializer="json")
        self.output_topic = self.app.topic(output_topic_name, value_serializer="json")

        self.window_duration_secs = window_duration_secs

        self.count = 0

        logger.info(f"Broker address: {broker_address}")
        logger.info(f"Input topic: {self.input_topic}")
        logger.info(f"Output topic: {self.output_topic}")
        logger.info(f"Window duration secs: {self.window_duration_secs}")

    def run(self):

        sdf = self.app.dataframe(topic=self.input_topic)


        '''
        Transform trade data to OHLC data
        '''

        def reduce_func(aggregated:dict, value:dict) -> dict:
            result = {
                "symbol": aggregated["symbol"],
                "open": aggregated["open"],
                "high": max(aggregated["high"], value["price"]),
                "low": min(aggregated["low"], value["price"]),
                "close": value["price"],
                "volume": aggregated["volume"] + float(value["qty"]),
                "timestamp_ms": value["timestamp_ms"]
            }

            return result

        def init_func(value:dict) -> dict:
            result = {
                "symbol": value["symbol"],
                "open": value["price"],
                "high": value["price"],
                "low": value["price"],
                "close": value["price"],
                "volume": float(value["qty"]),
                "timestamp_ms": value["timestamp_ms"]
            }
            return result

        sdf = sdf.group_by("symbol")
        sdf = sdf.tumbling_window(duration_ms=timedelta(seconds=self.window_duration_secs))
        sdf = sdf.reduce(reduce_func, init_func).final()


        sdf["symbol"] = sdf["value"]["symbol"]
        sdf["open"] = sdf["value"]["open"]
        sdf["close"] = sdf["value"]["close"]
        sdf["high"] = sdf["value"]["high"]
        sdf["low"] = sdf["value"]["low"]
        sdf["volume"] = sdf["value"]["volume"]
        sdf["timestamp_ms"] = sdf["value"]["timestamp_ms"]
        # For Debugging
        sdf["timestamp_ms_str"] = sdf["value"]["timestamp_ms"].apply(lambda val:datetime.fromtimestamp(val/1000).strftime('%Y-%m-%d %H:%M:%S'))

        sdf = sdf.to_topic(self.output_topic)

        def predict_and_expand(row: dict):
            self.count += 1
            print(f"Processing row {self.count}")
            print(row)

        sdf = sdf.apply(predict_and_expand)

        self.app.run(sdf)

if __name__ == "__main__":

    logger.remove()
    logger.add(sys.stdout,
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
               level="INFO")

    trade_to_ohlc = TradeToOhlc(config.broker_address, config.input_topic_name, config.output_topic_name, config.consumer_group, config.window_duration_secs)
    trade_to_ohlc.run()