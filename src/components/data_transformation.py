# Feature Engineering
# Handling Missing Values
# Outliers remove
# Handle imbalance dataset
# Convert categorical columns into numerical columns

from calendar import c
from math import isqrt
import os
import sys 
from src.logger import logging
from src.exception import CustomException
import numpy as np 
import pandas as pd 

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from  src.utils import save_object
@dataclass
class DataTransformationConfig:

    # create a folder in atifacts folder
    # here we will save our pickle file 
    preprocessor_obj_file_path= os.path.join("artifacts/data_transformation","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    

    # Function to get data , convert it and scale it
    def get_data_transformation_obj(self):

        try:
            logging.info("Data Transformation Started")

            numerical_features=['age', 'workclass', 'education.num', 'marital.status', 'occupation',
       'relationship', 'race', 'sex', 'capital.gain', 'capital.loss',
       'hours.per.week', 'native_country']

            # Numerical Pipeline 
            num_pipeline = Pipeline(
                steps=[

                    # This imputer fills the nulll values in our dataset to median
                    ("imputer" , SimpleImputer(strategy='median')),
                    # scaling the data . so all data remains in one unit
                    ("scaler",StandardScaler())
                ]
            )

            # # Categorical Pipeline
            # cat_pipeline = Pipeline(
            #     steps=[

            #         # This imputer fills the nulll values in our dataset to median
            #         ("imputer" , SimpleImputer(strategy='mode')),
            #         # scaling the data . so all data remains in one unit
            #         # ("scaler",StandardScaler()) we dont apply scaler on categorical feature 
            #     ]
            # )

            
            preprocessor = ColumnTransformer([
                # we will apply column transformer , with pipeline which we have defined above and input will be numerical_features 
                ("num_pipeline",num_pipeline , numerical_features)    
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    # Function to remove outlier
    def remove_outliers_IQR(self,col, df):
        try:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)

            # outlier formula 
            iqr = Q3 - Q1

            # upper limit and lower limit
            upper_limit = Q3 + 1.5 * iqr 
            lower_limit = Q1 - 1.5 * iqr 

            # data frame 
            # Ensure column is float to avoid dtype warning
            df[col] = df[col].astype(float)
            df.loc[(df[col] > upper_limit), col] = upper_limit
            df.loc[(df[col] < lower_limit), col] = lower_limit
            return df 

        except Exception as e:
            logging.info("Outliers handling code ")
            raise CustomException(e,sys)
    

    def inititate_data_transformation(self,train_path,test_path):
        try:
            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            numerical_features=['age', 'workclass', 'education.num', 'marital.status', 'occupation',
       'relationship', 'race', 'sex', 'capital.gain', 'capital.loss',
       'hours.per.week', 'native_country']
            
            for col in numerical_features:
                self.remove_outliers_IQR(col=col,df=train_data)

                logging.info("Outliers function on train data")

            for col in numerical_features:
                self.remove_outliers_IQR(col=col,df=test_data)

                logging.info("Outliers function on test data")

            preprocessor_obj=self.get_data_transformation_obj()

            target_columns="income"
            drop_columns = [target_columns]

            logging.info("Spliting data train into depndent and independent feature ")
            input_feature_train_data=train_data.drop(drop_columns, axis=1)
            target_feature_train_data=train_data[target_columns]

            logging.info("Spliting data test into depndent and independent feature ")
            input_feature_test_data=test_data.drop(drop_columns, axis=1)
            target_feature_test_data=test_data[target_columns]

            logging.info(" Data spliting completed. Inititializing Train Test Split")

            # apply transformation on our train and test data
            input_train_arr = preprocessor_obj.fit_transform(input_feature_train_data)
            input_test_arr = preprocessor_obj.transform(input_feature_test_data)
            
            logging.info("Train test completed ")
            # Preprocessor object on oir train data and test data
            train_array = np.c_[input_feature_train_data, np.array(target_feature_train_data)]
            test_array = np.c_[input_feature_test_data, np.array(target_feature_test_data)]



            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,
                        obj=preprocessor_obj)
            logging.info("Pickle file saved") 
            return(train_array,
                   test_array,
                   self.data_transformation_config.preprocessor_obj_file_path)
            
            
        except Exception as e:
            raise CustomException(e,sys)