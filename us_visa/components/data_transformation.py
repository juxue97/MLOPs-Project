import sys

import pandas as pd

from us_visa.constants import SCHEMA_FILE_PATH
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import read_yaml_file


class DataTransformation:
    def __init__(self,
                 dataIngestionArtifact: DataIngestionArtifact,
                 dataValidationArtifact: DataValidationArtifact,
                 dataTransformationConfig: DataTransformationConfig,
                 ):
        try:
            self.dataIngestionArtifact = dataIngestionArtifact
            self.dataValidationArtifact = dataValidationArtifact
            self.dataTransformationConfig = dataTransformationConfig
            self._schemaConfig = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)

    @staticmethod
    def _read_data(filePath: str) -> pd.DataFrame:
        try:
            dataFrame = pd.read_csv(filePath)
            return dataFrame
        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if self.dataValidationArtifact.validationStatus:
                logging.info("Initiating Data Transformation Process")
                trainDf = self._read_data(
                    filePath=self.dataIngestionArtifact.trainFilePath
                )
                testDf = self._read_data(
                    filePath=self.dataIngestionArtifact.testFilePath
                )

            else:
                raise Exception(self.dataValidationArtifact.message)

            dataTransformationArtifact = DataTransformationArtifact()
            return dataTransformationArtifact
        except Exception as e:
            raise USvisaException(e, sys) from e
