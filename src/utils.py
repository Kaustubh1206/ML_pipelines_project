# In utils file, we write helper function 
# this helps us to read data from github or yml file

import pickle
from src.logger import logging
from src.exception import CustomException
import os ,sys 

# This function is used to save picklefile, from any file where it is implmented to save it in artifacts folder
def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys) 