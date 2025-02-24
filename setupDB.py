import sys

from us_visa.utils.main_utils import download_dataset, read_dataset
from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import MONGO_DB_COLLECTION, MONGO_DB_NAME
from us_visa.exception import USvisaException


def upload_to_mongo(dataset_url: str) -> None:
    try:
        file_path = download_dataset(dataset=dataset_url)
        df = read_dataset(file_path=file_path)

        dict_data = df.to_dict(orient="records")

        mongoDBClient = MongoDBClient(MONGO_DB_NAME)
        col = mongoDBClient.database[MONGO_DB_COLLECTION]

        records = col.insert_many(dict_data)
        print("Done uploading csv data onto mongoDB")

    except Exception as e:
        raise USvisaException(e, sys)


if __name__ == "__main__":
    dataset_url = "moro23/easyvisa-dataset"
    upload_to_mongo(dataset_url)
