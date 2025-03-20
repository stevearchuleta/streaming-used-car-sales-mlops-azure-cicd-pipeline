
```md
# USED CAR SALES PRICE PREDICTION - AZURE MLOPS PIPELINE

## 1. Project Overview
This project provides an MLOps pipeline for predicting used car prices using a machine learning model. The model is trained using an **XGBoost Regressor**, which analyzes historical used car prices and related features such as **mileage, engine size, model year, and brand**. 

The pipeline is fully automated using **Azure Machine Learning (Azure ML)** for model training, evaluation, and deployment. **GitHub Actions is used for CI/CD automation**, ensuring that each model update is seamlessly integrated into the pipeline.

### Dataset Description
- **File Name:** `used_cars.csv`
- **Columns:**  
  - `price`: Target variable (continuous numeric value).  
  - `mileage`: The number of miles driven by the vehicle.  
  - `engine_size`: The size of the engine in liters.  
  - `year`: The model year of the car.  
  - `brand`: The manufacturer (categorical feature).  
- **Data Size:** Approximately **50,000 records** from used car listings.

---

## 2. Installation and Setup

### 1️⃣ Install Dependencies
Run the `setup.sh` script to install required Python dependencies:
```sh
bash setup.sh
```

### 2️⃣ Ensure Azure ML CLI is Installed
```sh
az extension add -n ml -y
```

---

## 3. Pipeline Workflow
The MLOps pipeline consists of the following key stages:

### 1️⃣ Preprocessing (`prep.py`)
- Loads `used_cars.csv` and cleans the data.
- Handles **missing values** using median imputation.
- Applies **log transformation** to `price` to normalize the distribution.
- Encodes categorical features (`brand`).
- Scales numerical features (`mileage`, `engine_size`, `year`).

### 2️⃣ Training (`train.py`)
- Trains an **XGBoost Regressor** model on the preprocessed dataset.
- Uses **RMSE, MSE, and R²** as evaluation metrics.

### 3️⃣ Evaluation (`train.py`)
- The model’s performance is **logged in MLflow**.
- Evaluation metrics can be accessed in **Azure ML Studio**.

### 4️⃣ Model Registration (`register.py`)
- Saves the trained model to **Azure ML** for deployment.
- Stores metadata about the registered model.

**Azure ML orchestrates job execution**, ensuring each step runs in the correct sequence.

---

## 4. How to Run the Pipeline

### Submit the MLOps Pipeline to Azure ML
Use the following command to submit the pipeline job:
```sh
bash run-job.sh mlops/azureml/train/newpipeline.yml used-car-sales-experiment
```
This command **submits an Azure ML job**, triggering preprocessing, training, evaluation, and model registration.

---

## 5. Folder and File Structure
This project follows **Azure MLOps best practices** with the following directory structure:

- `.github/workflows/` → Contains **CI/CD pipeline definitions** (`ci.yml`, `deploy-model-training-pipeline-classical.yml`).
- `data/` → Stores raw dataset (`used_cars.csv`).
- `data-science/src/` → Contains machine learning scripts (`prep.py`, `train.py`, `register.py`).
- `mlops/azureml/train/` → Stores Azure ML pipeline definitions (`newpipeline.yml`, `train.yml`).
- `jobs/pipeline/` → Contains `pipeline.yml`, which outlines the entire MLOps workflow.
- `requirements.txt` → Lists Python dependencies.
- `setup.sh` → Installs **Azure ML CLI tools**.
- `run-job.sh` → Submits the MLOps pipeline job.

---

## 6. CI/CD Automation with GitHub Actions
This project uses **GitHub Actions** to automate **model training and deployment**.

- `ci.yml` → Runs **pre-commit checks, unit tests, and formatting validation**.
- `deploy-model-training-pipeline-classical.yml` → Deploys the model to **Azure ML Pipelines**.
- Every push to `main` **triggers a training pipeline**.

---

## 7. Additional Notes
- This project follows **MLOps best practices for Azure**.
- Future improvements may include **hyperparameter tuning and real-time model monitoring**.
- To monitor jobs, navigate to **Azure ML Studio** and check job logs.
```

