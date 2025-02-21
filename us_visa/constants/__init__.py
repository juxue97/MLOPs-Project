import os

# MongoDB Configs
MONGO_DB_URL: str = os.getenv(
    "MONGODB_URL_KEY", "mongodb://root:rootpass@localhost:27017/?authSource=admin")
MONGO_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "US_VISA")
MONGO_DB_COLLECTION: str = os.getenv("MONGO_DB_COLLECTION", "visa_data")

# Common Configs
FILE_NAME: str = "usvisa.csv"
MODEL_FILE_NAME: str = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"

# Training Pipeline Configs
PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = "artifact"

# Data Ingestion Configs
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
TRAIN_TEST_SPLIT_RATIO: float = 0.75
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

# Data Validation Configs
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

# Data Transformation Configs
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
