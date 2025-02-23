import os

# MongoDB Configs
MONGO_DB_URL: str = os.getenv(
    "MONGODB_URL_KEY", "mongodb://root:rootpass@localhost:27017/?authSource=admin")
MONGO_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "US_VISA")
MONGO_DB_COLLECTION: str = os.getenv("MONGO_DB_COLLECTION", "visa_data")

# AWS S3 Configs
AWS_ACCESS_KEY_ID = os.getenv(
    "AWS_ACCESS_KEY_ID_ENV_KEY", "please-get-your-own"
)
AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY_ENV_KEY", "please-get-your-own"
)
REGION_NAME = os.getenv("AWS_REGION_NAME", "please-get-your-own")

# Common Configs
FILE_NAME: str = "usvisa.csv"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

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
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"

# Model Trainer Configs
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_FILE_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.8
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join(
    "config", "model.yaml"
)

# Model Evaluation Configs

MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME = "usvisa-model2025"
