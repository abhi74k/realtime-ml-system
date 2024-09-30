'''
Subscribes to a Kafka topic and writes the data to a Hopsworks feature store.
'''

from datetime import datetime
from quixstreams import Application
import json
from loguru import logger
import pandas as pd
import sys
from config import config
from hopsworks_writer import HopsworksWriter
import time

def kafka_to_feature_store(
        kafka_broker_address: str,
        kafka_topic_name: str,
        consumer_group: str,
        feature_group_name: str,
        feature_group_description: str,
        feature_group_version: int,
        project_name: str,
        api_key: str,
        batch_size: int,
        enable_logging: bool = False,
        flush_interval_secs: int = 0,
        is_online: bool = True
):
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=consumer_group,
        auto_offset_reset="earliest"
    )

    # Initialize the HopsworksWriter
    writer = HopsworksWriter(
        project_name=project_name,
        api_key_value=api_key,
        feature_group_name=feature_group_name,
        feature_group_description=feature_group_description,
        feature_group_version=feature_group_version,
        is_online=is_online
    )

    flush_time_secs = None

    with app.get_consumer() as consumer:
        consumer.subscribe(topics=[kafka_topic_name])

        buffer = []
        prev_flush_time_secs = 0

        while True:
            msg = consumer.poll(1)
            curr_secs = int(time.time())

            if msg is None:

                if(flush_time_secs is not None and len(buffer) > 0 and curr_secs - prev_flush_time_secs > flush_interval_secs):
                    logger.info("Flushing buffer due to inactivity")
                    flush_buffer(buffer, writer)
                    buffer = []
                    prev_flush_time_secs  = curr_secs
                continue

            elif msg.error():
                logger.error('Kafka error:', msg.error())
                continue

            # Binary message to dict
            value = msg.value() # Binary message
            value_str = value.decode('utf-8') # Convert to string
            value_dict= json.loads(value_str) # Convert to dict

            if enable_logging:
                logger.info(f"Received message: {value_dict}, buffer size: {len(buffer)}")

            # Remove the 'value' key
            del value_dict['value']

            if len(buffer) < batch_size or (curr_secs - prev_flush_time_secs) < flush_interval_secs:
                buffer.append(value_dict)
            else:
                logger.info("Batch full. Flushing buffer")
                flush_buffer(buffer, writer)
                buffer = []
                prev_flush_time_secs = curr_secs
                # Store the offset of the processed message on the Consumer
                # for the auto-commit mechanism.
                # It will send it to Kafka in the background.
                # Storing offset only after the message is processed enables at-least-once delivery
                # guarantees.
                consumer.store_offsets(message=msg)



def flush_buffer(buffer, writer):
    df = pd.DataFrame(buffer)
    writer.write_df(df)


if __name__ == "__main__":

    logger.remove()
    logger.add(sys.stdout,
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
               level="INFO")

    # Pretty print the config
    logger.info(f"config: {json.dumps(config.dict(), indent=4)}")

    is_online = False

    if config.online_or_offline == 'online':
        is_online = True
    elif config.online_or_offline == 'offline':
        is_online = False
    else:
        logger.error(f"Invalid value for ONLINE_OR_OFFLINE: {config.online_or_offline}")
        sys.exit(1)

    kafka_to_feature_store(
       config.broker_address,
       config.kafka_topic_name,
       config.consumer_group,
       config.feature_group_name,
       config.feature_group_description,
       config.feature_group_version,
       config.project_name,
       config.api_key,
       config.batch_size,
       config.enable_logging,
       config.flush_interval_secs,
       is_online
    )