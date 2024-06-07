# Import modules
import os
from pathlib import Path
import logging

# Configure logging to display the time and message
logging.basicConfig(level=logging.INFO,format="%(asctime)s: %(message)s:")

# List of files to be created along with their paths
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "experiment/trial.ipynb",
    "app.py"
]

# Iterate over each file path in the list
for file_path in list_of_files:
    file_path = Path(file_path)

    # Split the file path into directory and file name
    file_dir, file_name = os.path.split(file_path)

    # Check if the directory path is not empty
    if file_dir != "":
        # Create the directory if it doesn't exist
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating folder {file_dir} for the files {file_name}")

    # Check if the file does not exist or if it is empty
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        # Create an empty file
        with open(file_path,"w") as f:
            pass
        logging.info(f"Creating file {file_name}")
    else:
        logging.info(f"{file_name} already exists")