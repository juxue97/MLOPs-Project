import os
from dotenv import load_dotenv

# Relative path (if .env is in a parent folder)
env_path: str = "./.env"

load_dotenv(env_path)  # Load the .env file

# MongoDB Configs
MONGO_DB_URL: str = os.getenv(
    "MONGO_DB_URL_KEY", "DB-URL")
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "DB-NAME")
MONGO_DB_COLLECTION: str = os.getenv("MONGO_DB_COLLECTION", "DB-COL")

# AWS S3 Configs
AWS_ACCESS_KEY_ID: str = os.getenv(
    "AWS_ACCESS_KEY_ID_ENV_KEY", "please-get-your-own"
)
AWS_SECRET_ACCESS_KEY: str = os.getenv(
    "AWS_SECRET_ACCESS_KEY_ENV_KEY", "please-get-your-own"
)
REGION_NAME: str = os.getenv("AWS_REGION_NAME", "please-get-your-own")

# Common Configs
FILE_NAME: str = "usvisa.csv"
SCHEMA_FILE_PATH: str = os.path.join("config", "schema.yaml")

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
PREPROCSSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

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
MODEL_BUCKET_NAME: str = "ml-models-2025"

# Server Config, note that the app port need to conver to int!
APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", 8000))
