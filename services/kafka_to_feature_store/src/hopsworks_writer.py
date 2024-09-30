import hopsworks
import pandas as pd


class HopsworksWriter:

    def __init__(self,
                 project_name: str,
                 api_key_value: str,
                 feature_group_name: str,
                 feature_group_description: str,
                 feature_group_version: int,
                 is_online: bool):

        self.project_name = project_name
        self.api_key_value = api_key_value
        self.feature_group_name = feature_group_name
        self.feature_group_description = feature_group_description
        self.feature_group_version = feature_group_version
        self.is_online = is_online

    def write_dict(self, value_dict: dict):
        value_df = pd.DataFrame([value_dict])
        self.write_df(value_df)

    def write_df(self, value_df: pd.DataFrame):
        project = hopsworks.login(project=self.project_name,
                                api_key_value=self.api_key_value)

        feature_group = project.get_feature_store().get_or_create_feature_group(
            name=self.feature_group_name,
            version=self.feature_group_version,
            description=self.feature_group_description,
            primary_key=['symbol', 'timestamp_ms'],
            event_time='timestamp_ms',
            online_enabled=self.is_online
        )
        feature_group.insert(value_df, write_options={"start_offline_materialization": not self.is_online})