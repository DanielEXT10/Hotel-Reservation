import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb

from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml,load_data
from scipy.stats import randint
import sys

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining():
    def __init__(self,train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)
            
            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            X_train.columns = X_train.columns.str.replace('[^A-Za-z0-9_]+', '_', regex=True)
            X_test.columns = X_test.columns.str.replace('[^A-Za-z0-9_]+', '_', regex=True)

            logger.info("Data Splitted sucessfully for model training")

            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException("Filed on loading data", sys)
        
    def train_lgbm(self,X_train, y_train):
        try:
            logger.info("Initializing model")
            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting our Hyperparameter tunning")
            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter= self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs= self.random_search_params["n_jobs"],
                verbose= self.random_search_params["verbose"],
                scoring= self.random_search_params["scoring"]
            )

            logger.info("Starting Hyperparameter tuning")
            random_search.fit(X_train,y_train)

            logger.info("Hyperparameter tuning completed")
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters are: {best_params}")
            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error while Hyperparameter tunning {e}")
            raise CustomException("Filed on Hyperparameter tunning", sys)
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating our model")
            y_pred = model.predict(X_test)

            #Metrics
            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"accuracy Score {accuracy}")
            logger.info(f"Precision Score {precision}")
            logger.info(f"Recall Score {recall}")
            logger.info(f"F1 Score {f1}")

            return {
                "accuracy": accuracy,
                "precision" : precision,
                "recall" : recall,
                "f1 score" : f1
            }

        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException("Filed on evaluating model", sys)
        
    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info("saving model")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}")
        
        except Exception as e:
            logger.error(f"Error while saving the model {e}")
            raise CustomException("Filed on model saving", sys)
    
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting model training pipeline")

                logger.info("Starting our MLFlow experimentation")

                logger.info("Logging the training and testins dataset to MLFlow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path='datasets')

                X_train,y_train,X_test,y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train,y_train)
                metrics = self.evaluate_model(best_lgbm_model,X_test,y_test)
                self.save_model(best_lgbm_model)

                logger.info("Logging the model into MLFow")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging params and metrics to MLFlow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model Trianing succesfully completed")

        except Exception as e:
            logger.error(f"Error in the model training pipeline {e}")
            raise CustomException("Filed during model training pipeline", sys)

if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_OUTPUT)
    trainer.run()




        



