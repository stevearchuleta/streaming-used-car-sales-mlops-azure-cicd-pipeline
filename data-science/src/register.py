# ===============================================
# MODEL REGISTRATION SCRIPT FOR AZURE ML PIPELINE
# ===============================================
# =====================================================================================================================================================================================================================
# GENERALIZED NOTE:
# register.py is a general script that applies to all Azure mlops projects with the exact same syntax.
# register.py does not need to be modified per project.
# there is no need to specify project names inside register.py because register.py dynamically receives project-specific values from the command-line arguments (--model_name, --model_path, --model_info_output_path).
# use this exact register.py for all Azure MLOps projects moving forward.
# =====================================================================================================================================================================================================================
"""
Loads the trained model from the sweep job, registers it in MLflow, and writes model info as JSON.
"""

# ================
# IMPORT LIBRARIES
# ================
import argparse
import os
import json
import mlflow
from pathlib import Path

# ======================================
# FUNCTION: PARSE COMMAND-LINE ARGUMENTS
# ======================================
def parse_args():
    '''Parse input arguments for model name, model path, and model info output path'''

    parser = argparse.ArgumentParser("register")
    parser.add_argument("--model_name", type=str, help="Name under which model will be registered")
    parser.add_argument("--model_path", type=str, help="Path to trained model directory")
    parser.add_argument("--model_info_output_path", type=str, help="Path to write model info JSON")
    return parser.parse_args()

# ============================================
# FUNCTION: REGISTER TRAINED MODEL IN AZURE ML
# ============================================
def main(args):
    '''Loads the trained model, logs it in MLflow, and registers it in Azure ML'''

    print(f"Registering model: {args.model_name}")

    # ======================================
    # LOAD TRAINED MODEL FROM SPECIFIED PATH
    # ======================================
    model = mlflow.sklearn.load_model(args.model_path)

    # ================================
    # LOG MODEL IN MLFLOW FOR TRACKING
    # ================================
    mlflow.sklearn.log_model(model, args.model_name)

    # ==================================
    # REGISTER LOGGED MODEL USING MLFLOW
    # ==================================
    run_id = mlflow.active_run().info.run_id  # Get current MLflow run ID
    model_uri = f"runs:/{run_id}/{args.model_name}"  # Define model URI
    mlflow_model = mlflow.register_model(model_uri, args.model_name)  # Register model in Azure ML
    model_version = mlflow_model.version  # Get assigned model version

    # =============================
    # WRITE MODEL INFO TO JSON FILE
    # =============================
    print("Writing model metadata to JSON file")
    model_info = {"id": f"{args.model_name}:{model_version}"}
    output_path = os.path.join(args.model_info_output_path, "model_info.json")
    os.makedirs(args.model_info_output_path, exist_ok=True)

    with open(output_path, "w") as of:
        json.dump(model_info, of)

# ====================================================================
# SCRIPT ENTRY POINT: PARSE ARGUMENTS, REGISTER MODEL, AND LOG RESULTS
# ====================================================================
if __name__ == "__main__":

    mlflow.start_run()

    # ==== PARSE COMMAND-LINE ARGUMENTS ====
    args = parse_args()

    # ==== PRINT ARGUMENT VALUES FOR VERIFICATION ====
    lines = [
        f"Model name: {args.model_name}",
        f"Model path: {args.model_path}",
        f"Model info output path: {args.model_info_output_path}"
    ]

    for line in lines:
        print(line)

    # ==== EXECUTE MAIN FUNCTION ====
    main(args)

    mlflow.end_run()
