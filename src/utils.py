# In utils file, we write helper function 
# this helps us to read data from github or yml file

import pickle
from src.logger import logging
from src.exception import CustomException
import os ,sys 
from sklearn.metrics import accuracy_score,confusion_matrix,precision_recall_curve, f1_score, recall_score, precision_score
from sklearn.model_selection import GridSearchCV

# This function is used to save picklefile, from any file where it is implmented to save it in artifacts folder
def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys) 

def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_object:
            return pickle.load(file_object)
    except Exception as e:
        raise CustomException(e,sys)
    

# Evaluate model 
def evaluate_model(X_train,y_train,X_test,y_test,models,params):
    try:
        #emprty dict -> report 
        report = {}
        # run loop for all models
        for i in range(len(list(models))):
            # extracting the best values Of model 
            model = list(models.values())[i]
            # best parameters 
            para = params[list(models.keys())[i]]

            # hyper paramwter
            gs= GridSearchCV(model , para , cv=5)
            gs.fit(X_train, y_train)

            # set best best parameters
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            # make prediction 
            y_pred= model.predict(X_test)
            test_model_accuracy= accuracy_score(y_test,y_pred)

            # update report 
            report[list(models.values())[i]]=test_model_accuracy

            return report

    except Exception as e:
        raise CustomException(e,sys)
    