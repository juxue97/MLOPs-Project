import sys
import numpy as np
import pandas as pd
from datetime import date
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTEENN
from typing import Any, Tuple

from us_visa.constants import SCHEMA_FILE_PATH
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.estimator import TargetValueMapping
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.utils.main_utils import read_yaml_file, save_numpy_array_data, save_object

pd.set_option('future.no_silent_downcasting', True)


class DataTransformation:
    def __init__(self,
                 dataIngestionArtifact: DataIngestionArtifact,
                 dataValidationArtifact: DataValidationArtifact,
                 dataTransformationConfig: DataTransformationConfig,
                 ):
        try:
            self.dataIngestionArtifact = dataIngestionArtifact
            self.dataValidationArtifact = dataValidationArtifact
            self.dataTransformationConfig = dataTransformationConfig
            self._schemaConfig = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)

    @staticmethod
    def _read_data(filePath: str) -> pd.DataFrame:
        logging.info(f"Loading DataFrame from: {filePath}")
        try:
            dataFrame = pd.read_csv(filePath)
            return dataFrame
        except Exception as e:
            raise USvisaException(e, sys)

    def _preprocess_data(self, dataFrame: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        logging.info("Performing data preprocessing")
        try:
            # Separate X and y
            target_col = self._schemaConfig["target_columns"]
            drop_cols = self._schemaConfig["drop_columns"]

            inputFeaturesDf = dataFrame.drop(
                columns=target_col, axis=1
            )
            targetFeatureDf = dataFrame[self._schemaConfig["target_columns"]]

            # Convert the feature(s) into more meaningful feature
            todays_date = date.today()
            current_years = todays_date.year
            inputFeaturesDf["company_age"] = current_years - \
                inputFeaturesDf["yr_of_estab"]

            # Drop certain features
            inputFeaturesDf.drop(
                columns=drop_cols, inplace=True, axis=1
            )

            targetFeatureDf = targetFeatureDf.replace(
                TargetValueMapping()._asdict()
            ).infer_objects(copy=False)

            return inputFeaturesDf, targetFeatureDf

        except Exception as e:
            raise USvisaException(e, sys)

    def _get_data_transformer_object(self) -> ColumnTransformer:
        logging.info("Performing data transformation")
        try:
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()

            transform_columns = self._schemaConfig["transform_columns"]
            numerical_columns = self._schemaConfig["num_features"]
            # one-hot encoding
            oh_columns = self._schemaConfig["oh_columns"]
            # ordinal-encoding
            or_columns = self._schemaConfig["or_columns"]

            transform_pipe = Pipeline(steps=[
                ('transformer', PowerTransformer(method='yeo-johnson'))
            ])

            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", oh_transformer, oh_columns),
                    ("Ordinal_Encoder", ordinal_encoder, or_columns),
                    ("Transformer", transform_pipe, transform_columns),
                    ("StandardScaler", numeric_transformer, numerical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise USvisaException(e, sys)

    def _data_resampling(self, X: np.ndarray, y: pd.DataFrame) -> Tuple[pd.DataFrame | Any, pd.DataFrame | Any]:
        logging.info("Performing data resampling")
        try:
            smt = SMOTEENN(sampling_strategy='minority')

            inputFeatureTrainFinal, targetFeatureTrainFinal = smt.fit_resample(
                X, y
            )
            return inputFeatureTrainFinal, targetFeatureTrainFinal
        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if self.dataValidationArtifact.validationStatus:
                logging.info("Initiating Data Transformation Process")
                trainDf, testDf = (
                    self._read_data(
                        filePath=self.dataIngestionArtifact.trainFilePath
                    ),
                    self._read_data(
                        filePath=self.dataIngestionArtifact.testFilePath
                    ))
                # Preprocess
                X_train_df, y_train_df = self._preprocess_data(trainDf)
                X_test_df, y_test_df = self._preprocess_data(testDf)

                preprocessor = self._get_data_transformer_object()

                # Transformation
                X_train = preprocessor.fit_transform(X_train_df)
                X_test = preprocessor.transform(X_test_df)

                # Resampling
                inputFeatureTrainFinal, targetFeatureTrainFinal = self._data_resampling(
                    X_train, y_train_df
                )
                inputFeatureTestFinal, targetFeatureTestFinal = self._data_resampling(
                    X_test, y_test_df
                )

                # Save to np file
                train_arr = np.c_[
                    inputFeatureTrainFinal, np.array(targetFeatureTrainFinal)
                ]

                test_arr = np.c_[
                    inputFeatureTestFinal, np.array(targetFeatureTestFinal)
                ]

                save_object(
                    self.dataTransformationConfig.transformedObjectFilePath, preprocessor
                )
                save_numpy_array_data(
                    self.dataTransformationConfig.transformedTrainFilePath, array=train_arr
                )
                save_numpy_array_data(
                    self.dataTransformationConfig.transformedTestFilePath, array=test_arr
                )
                dataTransformationArtifact = DataTransformationArtifact(
                    transformedObjectFilePath=self.dataTransformationConfig.transformedObjectFilePath,
                    transformedTrainFilePath=self.dataTransformationConfig.transformedTrainFilePath,
                    transformedTestFilePath=self.dataTransformationConfig.transformedTestFilePath,
                )

                logging.info(
                    f"Data transformation artifact: {dataTransformationArtifact}")
                return dataTransformationArtifact

            else:
                raise Exception(self.dataValidationArtifact.message)

        except Exception as e:
            raise USvisaException(e, sys) from e
