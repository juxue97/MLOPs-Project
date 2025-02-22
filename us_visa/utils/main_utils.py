import sys
import dill
import kagglehub
import os
import numpy as np
import pandas as pd

from typing import Union

import yaml

from us_visa.exception import USvisaException
from us_visa.logger import logging


def download_dataset(dataset: str,
                     extensions: tuple[int] = (".csv", ".json", ".xlsx"),
                     ) -> Union[str | Exception]:
    """
    Downloads a dataset using kagglehub and returns the path to the first file
    matching the specified extensions.

    Args:
        dataset (str): The identifier of the dataset to download.
        extensions (tuple[int], optional): A tuple of file extensions to look for.
            Defaults to (".csv", ".json", ".xlsx").

    Returns:
        Union[str, Exception]: The path to the first file with a matching extension,
        or an Exception if no matching file is found or an error occurs during download.
    """
    try:
        path = kagglehub.dataset_download(dataset)

        for file in os.listdir(path):
            if file.endswith(extensions):
                return os.path.join(path, file)

        return Exception("no matching file found")

    except Exception as e:
        return Exception(f"error occur while attempt to download dataset: {e}")


def read_dataset(file_path: str) -> Union[pd.DataFrame | str | None]:
    """
    Reads a dataset from a specified file path and returns it as a DataFrame.

    Parameters:
        file_path (str): The path to the dataset file. Supported formats are CSV, JSON, and XLSX.

    Returns:
        pd.DataFrame | str | None: Returns a DataFrame if the file is successfully read.
        Returns a string message if the file path is invalid or unsupported.
        Returns None if the file path is empty.
    """

    # Step 4: Load the dataset into a DataFrame
    if file_path:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            df = pd.read_json(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            return "file_path cannot be empty!"

        return df

    else:
        return None


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise USvisaException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise USvisaException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of utils")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of utils")

    except Exception as e:
        raise USvisaException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise USvisaException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise USvisaException(e, sys) from e
