import os
import sys 
import logging 
from datetime import datetime

# We are giving the current time and format in which we want to log it
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Log path. where we want to store the log 
    # here - .getcwd will get the currect directory path. There we will create logs folder and will give the LOG_FILE
log_path=os.path.join(os.getcwd(),"logs", LOG_FILE)
os.makedirs(log_path, exist_ok=True) # this will help to make directory 

# Here we are joining the LOG_FILE (datetime) and log_path 
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)
logging.basicConfig(
    filename=LOG_FILE_PATH, # the file name 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", # The format in which we want to store or logs 
    level=logging.INFO
)

# if __name__ == "__main__":
#     logging.info("Logging started")