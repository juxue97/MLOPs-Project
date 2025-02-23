import sys
import numpy as np
from typing import Tuple
from neuro_mf import ModelFactory
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from us_visa.entity.artifact_entity import ClassificationMetricArtifact, DataTransformationArtifact, ModelTrainerArtifact
from us_visa.entity.config_entity import ModelTrainerConfig
from us_visa.entity.estimator import USvisaModel
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import load_numpy_array_data, load_object, save_object


class ModelTrainer:
    def __init__(self, dataTransformationArtifact: DataTransformationArtifact, modelTrainerConfig: ModelTrainerConfig):
        try:
            self.dataTransformationArtifact = dataTransformationArtifact
            self.modelTrainerConfig = modelTrainerConfig
        except Exception as e:
            raise USvisaException(e, sys)

    def _get_model_object_and_report(self, trainArr: np.array, testArr: np.array) -> Tuple[object, object]:
        try:
            logging.info("Performing model training")
            modelFactory = ModelFactory(
                model_config_path=self.modelTrainerConfig.modelConfigFilePath
            )

            X_train, y_train = trainArr[:, :-1], trainArr[:, -1]
            X_test, y_test = testArr[:, :-1], testArr[:, -1]

            bestModelDetail = modelFactory.get_best_model(
                X=X_train, y=y_train, base_accuracy=self.modelTrainerConfig.expectedAccuracy
            )

            modelObj = bestModelDetail.best_model

            logging.info("Generating report")

            y_pred = modelObj.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)

            metricArtifact = ClassificationMetricArtifact(
                accuracy=accuracy, f1_score=f1, precision_score=precision, recall_score=recall
            )

            return bestModelDetail, metricArtifact

        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Initiating Model Training Process")
            trainArr = load_numpy_array_data(
                file_path=self.dataTransformationArtifact.transformedTrainFilePath
            )
            testArr = load_numpy_array_data(
                file_path=self.dataTransformationArtifact.transformedTestFilePath
            )

            bestModelDetail, metricArtifact = self._get_model_object_and_report(
                trainArr=trainArr, testArr=testArr)

            preprocessingObj = load_object(
                file_path=self.dataTransformationArtifact.transformedObjectFilePath
            )

            if bestModelDetail.best_score < self.modelTrainerConfig.expectedAccuracy:
                logging.info(
                    "No models metrics was higher than the base score"
                )
                raise Exception(
                    "No models metrics was higher than the base score"
                )
            usvisa_model = USvisaModel(preprocessing_object=preprocessingObj,
                                       trained_model_object=bestModelDetail.best_model,
                                       )
            save_object(
                self.modelTrainerConfig.trainedModelFilePath, usvisa_model
            )

            modelTrainerArtifact = ModelTrainerArtifact(
                trainedModelFilePath=self.modelTrainerConfig.trainedModelFilePath,
                metricArtifact=metricArtifact,
            )

            logging.info(
                f"Model training artifact: {modelTrainerArtifact}")
            return modelTrainerArtifact
        except Exception as e:
            raise USvisaException(e, sys) from e
