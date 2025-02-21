import sys
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from us_visa.constants import SCHEMA_FILE_PATH
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file


class DataValidation():
    def __init__(self, dataIngestionArtifact: DataIngestionArtifact, dataValidationConfig: DataValidationConfig):
        try:
            self.dataIngestionArtifact = dataIngestionArtifact
            self.dataValidationConfig = dataValidationConfig
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)

    @staticmethod
    def read_data(filePath: str) -> pd.DataFrame:
        logging.info(f"Loading DataFrame from: {filePath}")
        try:
            return pd.read_csv(filePath)
        except Exception as e:
            raise USvisaException(e, sys)

    def _validate_number_of_columns(self, dataFrame: pd.DataFrame) -> bool:
        logging.info("Validating number of dataframe columns")
        try:
            return len(dataFrame.columns) == len(self._schema_config["columns"])
        except Exception as e:
            raise USvisaException(e, sys)

    def _validate_columns_format(self, dataFrame: pd.DataFrame) -> bool:
        logging.info("Validating types of dataframe columns")
        try:
            dfColumns = dataFrame.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dfColumns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns) > 0:
                logging.info(
                    f"Missing numerical column: {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dfColumns:
                    missing_categorical_columns.append(column)
            if len(missing_categorical_columns) > 0:
                logging.info(
                    f"Missing categorical column: {missing_categorical_columns}")

            return False if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0 else True

        except Exception as e:
            raise USvisaException(e, sys)

    def _detect_dataset_drift(self, referenceDf: pd.DataFrame, currentDf: pd.DataFrame) -> bool:
        logging.info("Checking DataDrift")
        try:
            dataDriftProfile = Report(metrics=[DataDriftPreset()])
            dataDriftProfile.run(
                reference_data=referenceDf, current_data=currentDf
            )

            jsonReport = dataDriftProfile.as_dict()
            write_yaml_file(
                file_path=self.dataValidationConfig.driftReportFilePath, content=jsonReport
            )

            n_features = jsonReport["metrics"][0]["result"]["number_of_columns"]
            n_drifted_features = jsonReport["metrics"][0]["result"]["number_of_drifted_columns"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            driftStatus = jsonReport["metrics"][0]["result"]["dataset_drift"]

            return driftStatus
        except Exception as e:
            raise USvisaException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Initiating Data Validation Process")
        try:
            # load the df
            trainDf, testDf = (
                DataValidation.read_data(
                    filePath=self.dataIngestionArtifact.trainFilePath),
                DataValidation.read_data(
                    filePath=self.dataIngestionArtifact.testFilePath),
            )
            validationErrorMessage = ""

            # validate the df # of columns
            status = self._validate_number_of_columns(trainDf)
            if not status:
                validationErrorMessage += f"Missing column(s) on train dataframe"
            status = self._validate_number_of_columns(testDf)
            if not status:
                validationErrorMessage += f"Missing column(s)"
            logging.info(
                "Compatible columns format on both train and test dataframe test dataframe")

            # validate types of column
            status = self._validate_columns_format(trainDf)
            if not status:
                validationErrorMessage += f"Incompatible train columns format"
            status = self._validate_columns_format(testDf)
            if not status:
                validationErrorMessage += f"Incompatible test columns format"

            validationStatus = len(validationErrorMessage) == 0

            if validationStatus:
                # Check data drift
                driftStatus = self._detect_dataset_drift(
                    referenceDf=trainDf, currentDf=testDf
                )
                if driftStatus:
                    logging.info("Drift detected")
                    validationErrorMessage = "Drift Detected"
                else:
                    validationErrorMessage = "Drift not detected"

            else:
                logging.info(f"Validation error: {validationErrorMessage}")

            dataValidationArtifact = DataValidationArtifact(
                validationStatus=validationStatus,
                message=validationErrorMessage,
                driftReportFilePath=self.dataValidationConfig.driftReportFilePath
            )

            logging.info(
                f"Data validation artifact: {dataValidationArtifact}")
            return dataValidationArtifact
        except Exception as e:
            raise USvisaException(e, sys)
