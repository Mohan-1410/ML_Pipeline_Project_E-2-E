import os, sys
import pandas as pd
import numpy as np
from SRC.logger import logging
from SRC.exceptions import CustomException
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from SRC.utils import save_object

@dataclass
class DataTransfrormationConfigs:
    preprocess_obj_file_patrh = os.path.join("artifacts/data_tranformation", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransfrormationConfigs()


    def get_data_transformation_obj(self):
        try:

            logging.info(" Data Transformation Started")

            numerical_features = ['age', 'workclass',  'education_num', 'marital_status',
            'occupation', 'relationship', 'race', 'sex', 'capital_gain',
            'capital_loss', 'hours_per_week', 'native_country']

            num_pipeline = Pipeline(
                steps = [
                ("imputer", SimpleImputer(strategy = 'median')),
                ("scaler", StandardScaler())

                
                ]
            )

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, numerical_features)
            ])

            return preprocessor


        except Exception as e:
            raise CustomException(e, sys)
        
    def remote_outliers_IQR(self, col, df):
        try:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)

            iqr = Q3 - Q1

            upper_limit = Q3 + 1.5 * iqr
            lowwer_limit = Q1 - 1.5 * iqr

            df.loc[(df[col]>upper_limit), col] = upper_limit
            df.loc[(df[col]<lowwer_limit), col] = lowwer_limit

            return df

        except Exception as e:
            logging.info("Outliers handling code")
            raise CustomException(e, sys)
        
    def inititate_data_transformation(self, train_path, test_path):

        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            numerical_features = ['age', 'workclass',  'education_num', 'marital_status',
            'occupation', 'relationship', 'race', 'sex', 'capital_gain',
            'capital_loss', 'hours_per_week', 'native_country']


            for col in numerical_features:
                self.remote_outliers_IQR(col = col, df = train_data)

            logging.info("Outliers capped on our train data")


            for col in numerical_features:
                self.remote_outliers_IQR(col = col, df = test_data)

            logging.info("Outliers capped on our test data")

            preprocess_obj = self.get_data_transformation_obj()

            traget_columns = "income"
            drop_columns = [traget_columns]

            logging.info("Splitting train data into dependent and independent features")
            input_feature_train_data = train_data.drop(drop_columns, axis = 1)
            traget_feature_train_data = train_data[traget_columns]

            logging.info("Splitting test data into dependent and independent features")
            input_feature_ttest_data = test_data.drop(drop_columns, axis = 1)
            traget_feature_test_data = test_data[traget_columns]

            # Apply transfpormation on our train data and test data
            input_train_arr = preprocess_obj.fit_transform(input_feature_train_data)
            input_test_arr = preprocess_obj.transform(input_feature_ttest_data)

            # Apply preprocessor object on our train data and test data
            train_array = np.c_[input_train_arr, np.array(traget_feature_train_data)]
            test_array = np.c_[input_test_arr, np.array(traget_feature_test_data)]


            save_object(file_path=self.data_transformation_config.preprocess_obj_file_patrh,
                        obj=preprocess_obj)
            
            return (train_array,
                    test_array,
                    self.data_transformation_config.preprocess_obj_file_patrh)

        except Exception as e:
            raise CustomException(e, sys)
