from flask import Flask
from src.logger import logging

# Flask app 
app=Flask(__name__)



@app.route('/',methods=['GET',"POST"])

# function 
def index():
    logging.info("WE are testing the second methods of logging")
    return " HELLO WORLD KAUSTUBH"

# TEsting
if __name__=="__main__":
    app.run(debug=True)