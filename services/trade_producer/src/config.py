# Use Pedantic for strict type checking

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv(find_dotenv())

class Config(BaseSettings):
    tickers: list = [
     "ETH/USD",
     "BTC/USD",
    ]
    mode: str = os.getenv("MODE", "realtime")
    from_time: str = os.getenv("FROM_TIME", "")
    to_time: str = os.getenv("TO_TIME", "")
    topic_name: str = os.getenv("TOPIC_NAME", "trades")

config = Config()