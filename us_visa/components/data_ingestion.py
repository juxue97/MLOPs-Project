import sys
import os

from pandas import DataFrame
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.utils.data_extract_utils import USVisaDataExtractionUtil
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, dataIngestionConfig: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.dataIngestionConfig = dataIngestionConfig
        except Exception as e:
            raise USvisaException(e, sys)

    def _export_data_into_feature_store(self) -> DataFrame:
        try:
            logging.info("Extracting data from mongoDB")
            data = USVisaDataExtractionUtil()
            dataFrame = data.export_collection_as_dataframe(
                collectionName=self.dataIngestionConfig.collectionName
            )
            featureStoreFilePath = self.dataIngestionConfig.featureStorePath
            dirPath = os.path.dirname(featureStoreFilePath)
            os.makedirs(dirPath, exist_ok=True)

            logging.info(
                f"Saving exported data into feature store file path: {featureStoreFilePath}")
            dataFrame.to_csv(featureStoreFilePath, index=False, header=True)

            # set the file path

            return dataFrame
        except Exception as e:
            raise USvisaException(e, sys)

    def _train_test_split(self, dataFrame: DataFrame) -> None:
        logging.info(
            f"Performing train-test-split for data {self.dataIngestionConfig.collectionName}")
        try:
            trainSet, testSet = train_test_split(
                dataFrame,
                train_size=self.dataIngestionConfig.trainTestSplitRatio,
                shuffle=True,
            )

            TrainTestFilePath = self.dataIngestionConfig.trainFilePath
            dirPath = os.path.dirname(TrainTestFilePath)
            os.makedirs(dirPath, exist_ok=True)

            logging.info(
                f"Saving train and test data into file path: {TrainTestFilePath}")
            trainSet.to_csv(self.dataIngestionConfig.trainFilePath,
                            index=False, header=True)
            testSet.to_csv(self.dataIngestionConfig.testFilePath,
                           index=False, header=True)

        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Initiating Data Ingestion Process")
        try:
            # Get data from db
            dataFrame = self._export_data_into_feature_store()

            # Perform train-test-split
            self._train_test_split(dataFrame=dataFrame)

            dataIngestionArtifact = DataIngestionArtifact(
                trainFilePath=self.dataIngestionConfig.trainFilePath,
                testFilePath=self.dataIngestionConfig.testFilePath
            )

            logging.info(f"Data ingestion artifact: {dataIngestionArtifact}")
            return dataIngestionArtifact

        except Exception as e:
            raise USvisaException(e, sys)
