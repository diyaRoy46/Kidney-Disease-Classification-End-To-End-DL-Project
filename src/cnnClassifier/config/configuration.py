from pathlib import Path

from cnnClassifier.utils.common import read_yaml, create_directories

from src.cnnClassifier.entity.config_entity import DataIngestionConfig


class ConfigurationManager:
    def __init__(self, config_filepath=Path("config/config.yaml")):
        self.config = read_yaml(config_filepath)
        create_directories([self.config.data_ingestion.root_dir])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        return DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source=config.source,
            local_data_file=Path(config.local_data_file),
            unzip_dir=Path(config.unzip_dir),
        )