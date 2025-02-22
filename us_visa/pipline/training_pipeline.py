import sys

from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_transformation import DataTransformation
from us_visa.components.data_validation import DataValidation
from us_visa.components.model_trainer import ModelTrainer
from us_visa.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig
from us_visa.logger import logging
from us_visa.entity.artifact_entity import (DataIngestionArtifact,
                                            DataTransformationArtifact,
                                            DataValidationArtifact,
                                            ModelPusherArtifact,
                                            ModelTrainerArtifact
                                            )
from us_visa.exception import USvisaException


class TrainPipeline:
    def __init__(self):
        try:
            self.dataIngestionConfig = DataIngestionConfig()
            self.dataValidationConfig = DataValidationConfig()
            self.dataTransformationConfig = DataTransformationConfig()
            self.modelTrainerConfig = ModelTrainerConfig()
        except Exception as e:
            raise USvisaException(e, sys) from e

    def _start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Running TrainingPipeline: data ingestion")
            dataIngestion = DataIngestion(
                dataIngestionConfig=self.dataIngestionConfig)
            dataIngestionArtifact = dataIngestion.initiate_data_ingestion()
            logging.info("Complete Process: data ingestion")

            return dataIngestionArtifact
        except Exception as e:
            raise USvisaException(e, sys) from e

    def _start_data_validation(self, dataIngestionArtifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Running TrainingPipeline: data validation")
            dataValidation = DataValidation(
                dataIngestionArtifact=dataIngestionArtifact,
                dataValidationConfig=self.dataValidationConfig,
            )
            dataValidationArtifact = dataValidation.initiate_data_validation()
            logging.info("Complete Process: data validation")

            return dataValidationArtifact
        except Exception as e:
            raise USvisaException(e, sys) from e

    def _start_data_transformation(self, dataIngestionArtifact: DataIngestionArtifact, dataValidationArtifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info("Running TrainingPipeline: data transformation")
            dataTransformation = DataTransformation(
                dataIngestionArtifact=dataIngestionArtifact,
                dataValidationArtifact=dataValidationArtifact,
                dataTransformationConfig=self.dataTransformationConfig,
            )
            dataTransformationArtifact = dataTransformation.initiate_data_transformation()
            logging.info("Complete Process: data transformation")

            return dataTransformationArtifact
        except Exception as e:
            raise USvisaException(e, sys) from e

    def _start_model_trainer(self, dataTransformationArtifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info("Running TrainingPipeline: Model Training")
            modelTrainer = ModelTrainer(dataTransformationArtifact=dataTransformationArtifact,
                                        modelTrainerConfig=self.modelTrainerConfig)
            modelTrainerArtifact = modelTrainer.initiate_model_trainer()
            logging.info("Complete Process: Model Training")

            return modelTrainerArtifact
        except Exception as e:
            raise USvisaException(e, sys) from e

    def _start_model_pushing(self) -> ModelPusherArtifact:
        try:
            pass
        except Exception as e:
            raise USvisaException(e, sys) from e

    def run_pipeline(self) -> None:
        try:
            # Start data ingestion:
            dataIngestionArtifact: DataIngestionArtifact = self._start_data_ingestion()

            # Start data validation:
            dataValidationArtifact: DataValidationArtifact = self._start_data_validation(
                dataIngestionArtifact=dataIngestionArtifact
            )

            # Start data transformation:
            dataTransformationArtifact: DataTransformationArtifact = self._start_data_transformation(
                dataIngestionArtifact=dataIngestionArtifact,
                dataValidationArtifact=dataValidationArtifact,
            )

            # Start model training:
            modelTrainerArtifact: ModelTrainerArtifact = self._start_model_trainer(
                dataTransformationArtifact=dataTransformationArtifact
            )

            # Start model evaluation:

            modelStatus = False
            if modelStatus:
                # Start model pushing:
                pass

        except Exception as e:
            raise USvisaException(e, sys) from e
