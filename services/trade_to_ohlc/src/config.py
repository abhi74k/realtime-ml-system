from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config(BaseSettings):
    input_topic_name: str = os.getenv("INPUT_TOPIC_NAME")
    output_topic_name: str = os.getenv("OUTPUT_TOPIC_NAME")
    broker_address: str = os.getenv("BROKER_ADDRESS", os.getenv("DEFAULT_BROKER_ADDRESS"))
    window_duration_secs: int = int(os.getenv("WINDOW_DURATION_SECS"))

config = Config()