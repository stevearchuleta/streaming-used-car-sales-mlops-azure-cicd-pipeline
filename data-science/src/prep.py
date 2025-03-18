# =======================================================
# DATA PREPROCESSING SCRIPT FOR USED CAR SALES PREDICTION
# =======================================================
"""
Cleans and prepares raw data for training and testing in the Used Car Sales prediction model.
"""

import argparse
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import numpy as np
import mlflow

# ==============================
# PARSE ARGUMENTS FOR FILE PATHS
# ==============================
def parse_args():
    parser = argparse.ArgumentParser("prep")
    parser.add_argument("--raw_data", type=str, help="Path to raw data")
    parser.add_argument("--train_data", type=str, help="Path to train dataset")
    parser.add_argument("--test_data", type=str, help="Path to test dataset")
    parser.add_argument("--test_train_ratio", type=float, default=0.2, help="Test-train ratio")
    return parser.parse_args()

# =========================================
# MAIN FUNCTION - DATA CLEANING & SPLITTING
# =========================================
def main(args):
    '''Read, clean, and split the dataset'''

    # ==== LOAD RAW DATA ====
    df = pd.read_csv(args.raw_data)

    # ==== HANDLE MISSING VALUES ====
    df.dropna(inplace=True)

    # ==== FEATURE SCALING ====
    scaler = StandardScaler()
    numeric_features = ["mileage", "engine_size", "year"]
    df[numeric_features] = scaler.fit_transform(df[numeric_features])

    # ==== LOG TRANSFORM FOR PRICE (HANDLES SKEWNESS) ====
    df["price"] = np.log1p(df["price"])

    # ==== TRAIN-TEST SPLIT ====
    train_df, test_df = train_test_split(df, test_size=args.test_train_ratio, random_state=42)

    # ==== SAVE TRAIN & TEST SETS ====
    os.makedirs(args.train_data, exist_ok=True)
    os.makedirs(args.test_data, exist_ok=True)
    train_df.to_csv(os.path.join(args.train_data, "train.csv"), index=False)
    test_df.to_csv(os.path.join(args.test_data, "test.csv"), index=False)

    # ==== LOG METRICS ====
    mlflow.log_metric("train size", train_df.shape[0])
    mlflow.log_metric("test size", test_df.shape[0])

# ==============
# EXECUTE SCRIPT
# ==============
if __name__ == "__main__":
    mlflow.start_run()
    args = parse_args()
    main(args)
    mlflow.end_run()
