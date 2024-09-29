from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv
from loguru import logger
import os

logger.info(f"find_dotenv(): {find_dotenv()}")

load_dotenv(find_dotenv())

class Config(BaseSettings):
    project_name: str = os.getenv("PROJECT_NAME")
    api_key: str = os.getenv("API_KEY_VALUE")
    feature_group_name: str = os.getenv("FEATURE_GROUP_NAME")
    feature_group_description: str = os.getenv("FEATURE_GROUP_DESCRIPTION")
    feature_group_version: str = os.getenv("FEATURE_GROUP_VERSION")

    kafka_topic_name: str = os.getenv("KAFKA_TOPIC_NAME")
    broker_address: str = os.getenv("BROKER_ADDRESS", os.getenv("DEFAULT_BROKER_ADDRESS"))
    consumer_group: str = os.getenv("CONSUMER_GROUP")
    enable_logging: bool = os.getenv("ENABLE_LOGGING", False)

    online_or_offline: str = os.getenv("ONLINE_OR_OFFLINE", "online")
    batch_size: int = os.getenv("BATCH_SIZE")

config = Config()