import os
from pathlib import Path
import logging # to log user actions


# loglevel to log user actions is INFO
# format is just in what format we want to log
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] : %(levelname)s - %(message)s")


list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "research/test.py",
    "app.py",
    "store_index.py",
    "static/.gitkeep",
    "templates/chat.html"
]

# loop through list of files and python will detect the path
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)# Separate folders from files

    if filedir !="": # if fildir is not empty
        os.makedirs(filedir, exist_ok=True)# Create file directory
        logging.info(f"Creating directory: {filedir} for the file: {filename}")
    
    # I have created folder now need to create file inside folder
    # if filepath does not exist I need to create it also will cheack size of the file 
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0): # if this file is not empty need to create that file
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    
    else:
        logging.info(f"{filename} already exists!")
    