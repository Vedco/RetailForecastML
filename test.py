import os
data_path = "data/processed/cleaned_data.csv"
# Check if the file exists at the given path
if os.path.exists(data_path):
    print(f"File found at {data_path}")
else:
    print(f"File not found at {data_path}")


