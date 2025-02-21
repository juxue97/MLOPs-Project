from dataclasses import dataclass
from datetime import datetime
import os

from us_visa.constants import *

TIMESTAMP: str = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipelineName: str = PIPELINE_NAME
    artifactDir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP


trainingPipelineConfig: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    trainTestSplitRatio: float = TRAIN_TEST_SPLIT_RATIO
    collectionName: str = MONGO_DB_COLLECTION
    dataIngestionDir: str = os.path.join(
        trainingPipelineConfig.artifactDir, DATA_INGESTION_DIR_NAME)
    featureStorePath: str = os.path.join(
        dataIngestionDir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    trainFilePath: str = os.path.join(
        dataIngestionDir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testFilePath: str = os.path.join(
        dataIngestionDir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
