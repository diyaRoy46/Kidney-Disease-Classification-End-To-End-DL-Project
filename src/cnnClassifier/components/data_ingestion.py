import os

from cnnClassifier.entity.config_entity import DataIngestionConfig
from cnnClassifier.utils.common import read_yaml, create_directories
from pathlib import Path
import os
import zipfile
import kagglehub

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

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            dataset_path = kagglehub.dataset_download(self.config.source)
            print(f"Dataset downloaded to: {dataset_path}")
            # kagglehub downloads and extracts automatically, copy to our local path
            import shutil
            shutil.make_archive(
                str(self.config.local_data_file).replace(".zip", ""),
                'zip',
                dataset_path
            )
            print(f"Archived dataset to: {self.config.local_data_file}")
        else:
            print(f"File already exists: {self.config.local_data_file}")

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        print(f"Extracted to: {unzip_path}")
try:
    config_manager = ConfigurationManager()
    data_ingestion_config = config_manager.get_data_ingestion_config()
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.extract_zip_file()
except Exception as e:
    raise e

