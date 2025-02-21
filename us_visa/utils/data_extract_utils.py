import sys
from typing import Optional

from us_visa.logger import logging
from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import MONGO_DB_NAME
from us_visa.exception import USvisaException
import pandas as pd
import numpy as np


class USVisaDataExtractionUtil:
    def __init__(self):
        try:
            self.mongoClient = MongoDBClient(databaseName=MONGO_DB_NAME)
        except Exception as e:
            raise USvisaException(e, sys) from e

    def export_collection_as_dataframe(self, collectionName: str, databaseName: Optional[str] = None) -> pd.DataFrame:
        logging.info("Exporting DB data into DataFrame")
        try:
            if databaseName is None:
                collection = self.mongoClient.database[collectionName]
            else:
                collection = self.mongoClient[databaseName][collectionName]

            data = collection.find()
            df = pd.DataFrame(list(data))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise USvisaException(e, sys) from e
