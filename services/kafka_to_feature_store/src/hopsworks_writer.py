import hopsworks
import pandas as pd


class HopsworksWriter:

    def __init__(self, 
                 project_name: str, 
                 api_key_value: str, 
                 feature_group_name: str, 
                 feature_group_description: str,
                 feature_group_version: int):
        
        self.project = hopsworks.login(project=project_name, 
                                      api_key_value=api_key_value)
        
        self.fs = self.project.get_feature_store()
        
        self.fg = self.fs.get_or_create_feature_group(
            name=feature_group_name,
            version=feature_group_version,
            description=feature_group_description,
            primary_key=['symbol', 'timestamp_end'],
            event_time='timestamp_end',
            online_enabled=True,
        )

    def write_dict(self, value_dict: dict):
        value_df = pd.DataFrame([value_dict])
        self.write_df(value_df)

    def write_df(self, value_df: pd.DataFrame):
        self.fg.insert(value_df)