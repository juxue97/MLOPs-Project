import sys
import pandas as pd

from us_visa.entity.config_entity import PredictConfig, USVisaPredictConfig
from us_visa.entity.s3_estimator import USVisaEstimator
from us_visa.exception import USvisaException
from us_visa.logger import logging


class USVisaClassifier:
    def __init__(self, predictionPipelineConfig: USVisaPredictConfig = USVisaPredictConfig()):
        try:
            self.predictionPipelineConfig = predictionPipelineConfig
        except Exception as e:
            raise USvisaException(e, sys) from e

    def get_payload_data_as_df(self, payload: PredictConfig) -> pd.DataFrame:
        try:
            logging.info("Converting payload dict into dataframe")
            payload_dict = {
                "continent": payload.continent,
                "education_of_employee": payload.education_of_employee,
                "has_job_experience": payload.has_job_experience,
                "region_of_employment": payload.region_of_employment,
                "unit_of_wage": payload.unit_of_wage,
                "full_time_position": payload.full_time_position,
                "no_of_employees": payload.no_of_employees,
                "company_age": payload.company_age,
                "prevailing_wage": payload.prevailing_wage,
            }

            df = pd.DataFrame([payload_dict])

            return df
        except Exception as e:
            raise USvisaException(e, sys) from e

    def predict(self, dataFrame: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Starting prediction pipeline")
            model = USVisaEstimator(
                bucketName=self.predictionPipelineConfig.model_bucket_name,
                modelPath=self.predictionPipelineConfig.model_file_path,
            )

            result = model.predict(dataFrame)

            logging.info(f"Complete process: prediction result {result}")
            return result
        except Exception as e:
            raise USvisaException(e, sys) from e
