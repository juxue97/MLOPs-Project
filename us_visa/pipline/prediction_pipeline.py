import sys

from us_visa.exception import USvisaException
from us_visa.logger import logging


class PredictionPipeline:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise USvisaException(e, sys) from e

    def run_pipeline(self):
        try:
            pass
        except Exception as e:
            raise USvisaException(e, sys) from e
