import os, sys
import pandas as pd
import numpy as np 
from SRC.logger import logging 
from SRC.exceptions import CustomException
from dataclasses import dataclass
from sklearn.model_selection import train_test_split 
from SRC.Components.data_transformation import DataTransformation

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join("artifacts/data_ingestion", "train.csv")
    test_data_path = os.path.join("artifacts/data_ingestion", "test.csv")
    raw_data_path = os.path.join("artifacts/data_ingestion", "raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_confi= DataIngestionConfig

    def initiate_data_ingestion(self):

        logging.info("Data Ingestion Started")

        try:
            logging.info("Data Reading using Pandas library from local system")
            data= pd.read_csv(os.path.join("Machine_Learning_project.egg-info\Data\income_cleandata.csv"))
            logging.info("Data Reading completed")
            os.makedirs(os.path.dirname(self.ingestion_confi.raw_data_path), exist_ok=True)
            data.to_csv(self.ingestion_confi.raw_data_path, index=False)
            logging.info("Data splitted into train and test")

            train_set, test_set = train_test_split(data, test_size= .30, random_state= 42)

            train_set.to_csv(self.ingestion_confi.train_data_path, index=  False, header=True)
            test_set.to_csv(self.ingestion_confi.test_data_path, index=  False, header=True)

            logging.info("Data Ingestion Completed")

            return (
                self.ingestion_confi.train_data_path,
                self.ingestion_confi.test_data_path

            )
            
        except Exception as e:
            logging.info("Error occurred in data ingestion stage")
        
            raise CustomException(e,sys)

if __name__=="__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.inititate_data_transformation(train_data_path, test_data_path)
