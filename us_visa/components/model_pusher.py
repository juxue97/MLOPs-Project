import sys

from us_visa.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.s3_estimator import USVisaEstimator
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.store.aws_s3_storage import SimpleStorageService


class ModelPusher:
    def __init__(self, modelPusherConfig: ModelPusherConfig, modelEvaluationArtifact=ModelEvaluationArtifact):
        try:
            self.modelPusherConfig = modelPusherConfig
            self.modelEvaluationArtifact = modelEvaluationArtifact
            self.s3 = SimpleStorageService()
            self.usVisaEstimator = USVisaEstimator(bucketName=modelPusherConfig.bucketName,
                                                   modelPath=modelPusherConfig.s3ModelKeyPath)
        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_model_pushing(self) -> ModelPusherArtifact:
        try:
            logging.info("Initiating Model Pushing Process")

            logging.info("Uploading model to s3 storage")
            self.usVisaEstimator.save_model(
                from_file=self.modelEvaluationArtifact.trainedModelPath
            )

            modelPusherArtifact = ModelPusherArtifact(
                bucketName=self.modelPusherConfig.bucketName,
                s3ModelPath=self.modelPusherConfig.s3ModelKeyPath
            )

            logging.info(
                f"Model pusher artifact: {modelPusherArtifact}")

            return modelPusherArtifact
        except Exception as e:
            raise USvisaException(e, sys) from e
