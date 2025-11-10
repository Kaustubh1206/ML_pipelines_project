from email import header
import os 
import sys 
import pandas as pd
import numpy as np 
from src.components import data_transformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from sklearn.model_selection import train_test_split 


# Data Ingestion 
@dataclass # Decorator
class DataIngestionConfig:
    # here we are creating folder artifacts and storing these csv
    # the data can be taken from clouds or local dataset 
    train_data_path=os.path.join('artifacts/data_ingestion','train.csv')
    test_data_path=os.path.join('artifacts/data_ingestion','test.csv')
    raw_data_path=os.path.join('artifacts/data_ingestion','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig() # we will call the DataIngestionConfig as we have to create artifacts and csv in folder

    def inititate_data_ingestion(self):
        try:        

            logging.info("Dataingestion inititated")
            # This only work on your local machine ( HARDCODED ). but if you want to run it on different machine 
                #data=pd.read_csv(os.path.join("/Users/kaustubh/Desktop/ML_Pipeline_Project/notebook/data/income_cleandata.csv"))


            # This work on any machine. and perfect for pipeline                
            data=pd.read_csv(os.path.join("notebook/data","cleandata.csv"))

            logging.info("Data read")
                # Creating artifacts folder
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)

            logging.info("Data converted to raw")
            # Train Test Split
            train_set, test_set= train_test_split(data, test_size=0.30 , random_state=42)
            logging.info("Data is splited into train and test")
            # split data is converted to csv file 
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data Ingestion completed")
            # returm train and test data
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )


        except Exception as e:
            logging.info("Error occured in data ingestion stage")
            raise CustomException(e,sys)
         
if __name__ == "__main__":
    obj= DataIngestion()
    train_data_path, test_data_path = obj.inititate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr, test_arr,  _ = data_transformation.inititate_data_transformation( train_data_path, test_data_path)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))