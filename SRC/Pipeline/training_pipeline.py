import os, sys
from SRC.logger import logging
from SRC.exceptions import CustomException
from SRC.Components.data_ingestion import DataIngestion
from SRC.Components.data_transformation import DataTransformation
from SRC.Components.model_trainer import ModelTrainer
from dataclasses import dataclass

if __name__ == "__main__":
    obj = DataIngestion()
    train_data_path, test_data_path = obj.inititate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.inititate_data_transformation(train_data_path, test_data_path)
    model_training = ModelTrainer()
    model_training.inititate_model_trainer(train_arr, test_arr)

    # src\pipeline\training_pipeline.py