from flask import Flask
from src.logger import logging
from src.exception import CustomException
import os , sys 
# Flask app 
app=Flask(__name__)



@app.route('/',methods=['GET',"POST"])

# function 
def index():
    try:
        logging.info("WE are testing the second methods of logging")
        raise Exception("HELLO WORLD KAUSTUBH, we are testing custom file ")
    
    except Exception as e:
        abc = CustomException(e, sys)
        logging.info(abc.error_message)
        return "welcome "



# TEsting
if __name__=="__main__":
    app.run(debug=True)