import kagglehub
import pandas as pd
import os

# Step 1: Download the dataset
dataset = "moro23/easyvisa-dataset"
path = kagglehub.dataset_download(dataset)

print(f"Dataset downloaded to: {path}")

# Step 2: List available files
files = os.listdir(path)
print(f"Files in dataset: {files}")

# Step 3: Identify the dataset file (CSV, JSON, or Excel)
def get_data_file(directory, extensions=(".csv", ".json", ".xlsx")):
    for file in os.listdir(directory):
        if file.endswith(extensions):
            return os.path.join(directory, file)  # Return the full file path
    return None  # Return None if no valid file is found

file_path = get_data_file(path)

# Step 4: Load the dataset into a DataFrame
if file_path:
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        df = pd.read_json(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    
    print(f"Loaded dataset ({os.path.basename(file_path)}):")
    print(df.head())  # Display first few rows
else:
    print("No supported dataset file found.")
