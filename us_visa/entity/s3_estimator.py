import sys
from pandas import DataFrame

from us_visa.cloud_storage.aws_storage import SimpleStorageService
from us_visa.exception import USvisaException
from us_visa.entity.estimator import USvisaModel


class USVisaEstimator:
    """
    This class is used to save and retrieve us_visas model in s3 bucket and to do prediction
    """

    def __init__(self, bucketName, modelPath,):
        """
        :param bucketName: Name of your model bucket
        :param modelPath: Location of your model in bucket
        """
        self.bucketName = bucketName
        self.s3 = SimpleStorageService()
        self.modelPath = modelPath
        self.loaded_model: USvisaModel = None

    def is_model_present(self, modelPath):
        try:
            return self.s3.s3_key_path_available(bucketName=self.bucketName, s3_key=modelPath)
        except USvisaException as e:
            print(e)
            return False

    def load_model(self,) -> USvisaModel:
        """
        Load the model from the modelPath
        :return:
        """

        return self.s3.load_model(self.modelPath, bucketName=self.bucketName)

    def save_model(self, from_file, remove: bool = False) -> None:
        """
        Save the model to the modelPath
        :param from_file: Your local system model path
        :param remove: By default it is false that mean you will have your model locally available in your system folder
        :return:
        """
        try:
            self.s3.upload_file(from_file,
                                to_filename=self.modelPath,
                                bucketName=self.bucketName,
                                remove=remove
                                )
        except Exception as e:
            raise USvisaException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        :param dataframe:
        :return:
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise USvisaException(e, sys)
