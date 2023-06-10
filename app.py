from flask import Flask
from SRC.logger import logging 
from SRC.exceptions import CustomException
import os , sys

app= Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
    try:
        raise Exception ("We are testing our custom file")
    except Exception as e:
        abc=CustomException(e,sys)
        logging.info("We are testing our second method of logging")
        return "Welcome to Mohan's ML Project"

if __name__=="__main__":
    app.run(debug=True)

