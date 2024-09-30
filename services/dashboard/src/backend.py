

import hopsworks
from config import config
from loguru import logger

def test(project_name, api_key_value, feature_group_name, feature_group_version, feature_view_name, feature_view_version):

    project = hopsworks.login(project=project_name,
                              api_key_value=api_key_value)

    logger.info("Logged in to Hopsworks")

    fs = project.get_feature_store()

    ohlc_10_fg = fs.get_feature_group(feature_group_name, feature_group_version)
    logger.info(f"Got feature group: {feature_group_name}")

    view_query = ohlc_10_fg.select_all()

    feature_view = fs.get_or_create_feature_view(
        name=feature_view_name,
        version=feature_view_version,
        query=view_query
    )
    logger.info(f"Got feature view: {feature_view_name}")

    data = feature_view.get_batch_data()

    print(data.head())

    return data

def get_data():
    return test(config.project_name,
                config.api_key,
                config.feature_group_name,
                config.feature_group_version,
                config.feature_view_name,
                config.feature_view_version)

if __name__ == "__main__":

    # Log the configuration
    logger.info(f"config: {config.dict()}")

    test(config.project_name,
         config.api_key,
         config.feature_group_name,
         config.feature_group_version,
         config.feature_view_name,
         config.feature_view_version)