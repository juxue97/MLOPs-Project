import sys
from dataclasses import dataclass
import pandas as pd
from typing import Optional
from datetime import date
import numpy as np

from sklearn.metrics import f1_score

from us_visa.constants import SCHEMA_FILE_PATH
from us_visa.entity.artifact_entity import DataIngestionArtifact, ModelEvaluationArtifact, ModelTrainerArtifact
from us_visa.entity.config_entity import ModelEvaluationConfig
from us_visa.entity.estimator import TargetValueMapping
from us_visa.entity.s3_estimator import USVisaEstimator
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import read_yaml_file


@dataclass
class EvaluateModelResponse:
    trainedModelF1Score: float
    bestModelF1Score: float
    isModelAccepted: bool
    difference: float


class ModelEvaluator:
    def __init__(self,
                 dataIngestionArtifact: DataIngestionArtifact,
                 modelTrainerArtifact: ModelTrainerArtifact,
                 modelEvaluationConfig: ModelEvaluationConfig,
                 ):
        try:
            self.modelEvaluationConfig = modelEvaluationConfig
            self.modelTrainerArtifact = modelTrainerArtifact
            self.dataIngestionArtifact = dataIngestionArtifact
            self._schemaConfig = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)

    def _get_best_model(self) -> Optional[USVisaEstimator]:
        try:
            logging.info("Retrieving model from s3 storage")

            bucketName = self.modelEvaluationConfig.bucketName
            modelPath = self.modelEvaluationConfig.s3ModelKeyPath
            estimator = USVisaEstimator(
                bucketName=bucketName, modelPath=modelPath
            )

            if estimator.is_model_present(modelPath=modelPath):
                return estimator
            return None
        except Exception as e:
            raise USvisaException(e, sys)

    def _evaluate_model(self) -> EvaluateModelResponse:
        try:
            logging.info("Evaluating trained model and previous model")

            currentYear = date.today().year
            testDf = pd.read_csv(self.dataIngestionArtifact.testFilePath)
            testDf["company_age"] = currentYear - testDf["yr_of_estab"]

            # Note that this is a list, not string
            targetColumn = self._schemaConfig["target_columns"]

            X = testDf.drop(columns=targetColumn, axis=1)
            y = testDf[targetColumn[0]]

            y = y.replace(
                TargetValueMapping()._asdict()
            )

            trainedModelF1Score = self.modelTrainerArtifact.metricArtifact.f1_score

            bestModelF1Score = None
            bestModel = self._get_best_model()
            if bestModel is not None:
                y = np.array(y).ravel().astype(int)
                yHatBestModel = bestModel.predict(X).astype(int)

                bestModelF1Score = f1_score(y, yHatBestModel)

            tmpBestModelScore = 0 if bestModelF1Score is None else bestModelF1Score
            result = EvaluateModelResponse(trainedModelF1Score=trainedModelF1Score,
                                           bestModelF1Score=bestModelF1Score,
                                           isModelAccepted=trainedModelF1Score > tmpBestModelScore,
                                           difference=trainedModelF1Score - tmpBestModelScore
                                           )
            logging.info(f"Result: {result}")
            return result

        except Exception as e:
            raise USvisaException(e, sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info("Initiating Model Evaluation Process")
            response = self._evaluate_model()

            modelEvaluationArtifact = ModelEvaluationArtifact(
                isModelAccepted=response.isModelAccepted,
                s3ModelPath=self.modelEvaluationConfig.s3ModelKeyPath,
                trainedModelPath=self.modelTrainerArtifact.trainedModelFilePath,
                changedAccuracy=response.difference,
            )

            logging.info(
                f"Model evaluation artifact: {modelEvaluationArtifact}")
            return modelEvaluationArtifact
        except Exception as e:
            raise USvisaException(e, sys) from e
