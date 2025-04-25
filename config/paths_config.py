import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
########################## Data Ingestion ##########################

RAW_DIR = PROJECT_ROOT / "artifacts" / "raw"
RAW_FILE_PATH = RAW_DIR / "raw.csv"
TRAIN_FILE_PATH = RAW_DIR / "train.csv"
TEST_FILE_PATH = RAW_DIR / "test.csv"



# Points to the root of the project, even from inside /src

CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

############################## DATA PROCESSING ######################

PROCESSED_DIR = PROJECT_ROOT / "artifacts" / "processed"
PROCESSED_TRAIN_DATA_PATH = PROCESSED_DIR / "processed_train.csv"
PROCESSED_TEST_DATA_PATH = PROCESSED_DIR / "processed_test.csv"

############################# Model training #################################

MODEL_OUTPUT = PROJECT_ROOT / "artifacts" / "models" / "lgbm_model.pkl"