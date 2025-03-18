# ===================================================
# TRAINING SCRIPT FOR USED CAR SALES PRICE PREDICTION
# ===================================================
"""
Trains an XGBoost Regressor model to predict Used Car Prices and evaluates it using RMSE, MSE, and R².
"""

import argparse
import os
import pandas as pd
import mlflow
import mlflow.sklearn
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score

# ==============================
# PARSE ARGUMENTS FOR FILE PATHS
# ==============================
def parse_args():
    parser = argparse.ArgumentParser("train")
    parser.add_argument("--train_data", type=str, help="Path to train dataset")
    parser.add_argument("--test_data", type=str, help="Path to test dataset")
    parser.add_argument("--model_output", type=str, help="Path of output model")
    return parser.parse_args()

# ======================================
# MAIN FUNCTION - TRAIN & EVALUATE MODEL
# ======================================
def main(args):
    '''Read train and test datasets, train model, evaluate model, save trained model'''

    # ==== READ TRAIN AND TEST DATA ====
    train_df = pd.read_csv(os.path.join(args.train_data, "train.csv"))
    test_df = pd.read_csv(os.path.join(args.test_data, "test.csv"))

    # ==== SPLIT FEATURES AND TARGET ====
    y_train = train_df["price"]
    X_train = train_df.drop(columns=["price"])
    y_test = test_df["price"]
    X_test = test_df.drop(columns=["price"])

    # ==== TRAIN XGBOOST REGRESSOR ====
    model = xgb.XGBRegressor()
    model.fit(X_train, y_train)

    # ==== PREDICT ON TEST DATA ====
    yhat_test = model.predict(X_test)

    # ==== COMPUTE EVALUATION METRICS ====
    rmse = mean_squared_error(y_test, yhat_test, squared=False)
    mse = mean_squared_error(y_test, yhat_test)
    r2 = r2_score(y_test, yhat_test)

    print(f"RMSE: {rmse:.4f}, MSE: {mse:.4f}, R²: {r2:.4f}")

    # ==== LOG METRICS ====
    mlflow.log_metric("RMSE", rmse)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("R2", r2)

    # ==== SAVE THE MODEL ====
    mlflow.sklearn.save_model(sk_model=model, path=args.model_output)

# ==============
# EXECUTE SCRIPT
# ==============
if __name__ == "__main__":
    mlflow.start_run()
    args = parse_args()
    main(args)
    mlflow.end_run()
