import os 
import sys 
from src.logger import logging



def error_message_details(error,error_details:sys):
    _,_, exc_tb = error_details.exc_info() # exc_tb -> execution try block. it starts executing code from first line
                                            # exc_info -> execution information  

                # tb_frame -> one by one line  
                # f_code ->  from where and which line error or exception occured 
                # co_filename -> it executes all the function in every file                            
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error Occurs in python script name[{0}] line number [{1}] error message[{2}]".format(
        file_name, # error occured in which file 
        exc_tb.tb_lineno, # in which line 
        str(error) # file no.
    )

    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_message)

        # calling error message details function which we have created 
        self.error_message=error_message_details(error_message, error_details = error_details) # here we will take error_message and error_details


    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Division by zero")
        raise CustomException(e,sys) # error message , error details
 