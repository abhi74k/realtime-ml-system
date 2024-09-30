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
    feature_group_version: int = os.getenv("FEATURE_GROUP_VERSION")

    feature_view_name: str = os.getenv("FEATURE_VIEW_NAME")
    feature_view_version: int = os.getenv("FEATURE_VIEW_VERSION")

config = Config()