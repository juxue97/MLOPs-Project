import pymongo
import certifi
import sys

from us_visa.constants import MONGO_DB_URL
from us_visa.logger import logging
from us_visa.exception import USvisaException

# Encrypt the data transmit between program and db (TSL)
# ca = certifi.where()


class MongoDBClient:
    client = None

    def __init__(self, databaseName: str):
        try:
            if MongoDBClient.client is None:
                mongoDBUrl = MONGO_DB_URL
                if mongoDBUrl is None:
                    raise Exception("Environment key: MONGO_DB_URL is not set")
                MongoDBClient.client = pymongo.MongoClient(host=mongoDBUrl)

            self.client = MongoDBClient.client
            self.database = self.client[databaseName]
            logging.info("MongoDB connection successful")

        except Exception as e:
            raise USvisaException(e, sys) from e
