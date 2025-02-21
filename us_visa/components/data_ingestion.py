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
    def __init__(self, dataIngestionConfig: DataIngestionConfig):
        try:
            self.dataIngestionConfig = dataIngestionConfig
        except Exception as e:
            raise USvisaException(e, sys)

    def _export_data_into_feature_store(self) -> DataFrame:
        """
        Exports data from a MongoDB collection to a CSV file in the feature store.

        This method extracts data from a specified MongoDB collection, converts it
        into a DataFrame, and saves it as a CSV file at the path defined in the
        DataIngestionConfig. If the directory for the feature store does not exist,
        it is created.

        Returns:
            DataFrame: The DataFrame containing the exported data.

        Raises:
            USvisaException: If an error occurs during data extraction or file saving.
        """

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

            return dataFrame
        except Exception as e:
            raise USvisaException(e, sys)

    def _train_test_split(self, dataFrame: DataFrame) -> None:
        """
        Splits the given DataFrame into training and testing datasets based on the
        configuration specified in DataIngestionConfig. Saves the resulting datasets
        as CSV files to the paths defined in the configuration.

        Args:
            dataFrame (DataFrame): The DataFrame to be split into train and test sets.

        Raises:
            USvisaException: If an error occurs during the train-test split or file
            saving process.
        """

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
        """
        Handles the data ingestion process for the US Visa application, including
        exporting data from MongoDB to a feature store and performing a train-test
        split. Utilizes the DataIngestionConfig for configuration settings and
        returns a DataIngestionArtifact containing file paths for the train and test
        datasets.

        Attributes:
            dataIngestionConfig (DataIngestionConfig): Configuration for data
            ingestion, including paths and split ratio.

        Methods:
            _export_data_into_feature_store() -> DataFrame:
                Exports data from MongoDB to a CSV file in the feature store.
            _train_test_split(dataFrame: DataFrame) -> None:
                Splits the data into train and test sets and saves them to CSV files.
            initiate_data_ingestion() -> DataIngestionArtifact:
                Initiates the data ingestion process and returns an artifact with
                train and test file paths.
        """

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
