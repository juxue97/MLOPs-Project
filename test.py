from us_visa.logger import logging
from us_visa.utils.main_utils import download_dataset,read_dataset

dataset_url = "moro23/easyvisa-dataset"

file_path = download_dataset(dataset=dataset_url)
df = read_dataset(file_path=file_path)

print(df)
logging.info("df successfully download and run")
