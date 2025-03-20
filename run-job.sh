#!/bin/bash

# ========================================================================================
# AZURE ML JOB EXECUTION SCRIPT FOR MACHINE LEARNING PIPELINE
# ========================================================================================
# This script is responsible for executing Azure ML pipeline jobs from the command line.
# It creates an ML job using a provided pipeline YAML file and monitors the job execution.
# ========================================================================================

# =====================
# PARSE INPUT ARGUMENTS
# =====================
job=$1  # ==== YAML FILE CONTAINING JOB DEFINITION ====
experiment_name=$2  # ==== (OPTIONAL) SPECIFY EXPERIMENT NAME ====
option=$3  # ==== (OPTIONAL) FLAG TO CONTROL WAITING FOR JOB COMPLETION ====

# ===========================
# ENSURE JOB FILE IS PROVIDED
# ===========================
if [[ -z "$job" ]]; then
  echo "Error: Job file is not specified."
  exit 1
fi

# ===================
# CREATE AZURE ML JOB
# ===================
if [[ -z "$experiment_name" ]]; then
  if [[ "$job" =~ pipeline.yml ]]; then
    run_id=$(az ml job create -f "$job" --query name -o tsv --set settings.force_rerun=True)
  else
    run_id=$(az ml job create -f "$job" --query name -o tsv)
  fi
else
  run_id=$(az ml job create -f "$job" --query name -o tsv --set experiment_name="$experiment_name" --set settings.force_rerun=True)
fi

# ====================================
# CHECK IF JOB CREATION WAS SUCCESSFUL
# ====================================
if [[ -z "$run_id" ]]; then
  echo "Error: Job creation failed. Check if your pipeline YAML is valid."
  exit 3
fi

# ===============================================
# OPTION TO EXIT IMMEDIATELY AFTER JOB SUBMISSION
# ===============================================
if [[ "$option" == "nowait" ]]; then
  az ml job show -n "$run_id" --query services.Studio.endpoint
  exit 0
fi

# ===================================
# MONITOR JOB STATUS UNTIL COMPLETION
# ===================================
status=$(az ml job show -n "$run_id" --query status -o tsv)
if [[ -z "$status" ]]; then
  echo "Error: Failed to retrieve job status."
  exit 4
fi

# ===============================
# RETRIEVE JOB URI FOR MONITORING
# ===============================
job_uri=$(az ml job show -n "$run_id" --query services.Studio.endpoint)
if [[ -z "$job_uri" ]]; then
  echo "Error: Failed to retrieve job URI."
  exit 5
fi

echo "Job URI: $job_uri"

# =======================================
# DEFINE STATUS STATES FOR JOB MONITORING
# =======================================
running=("Queued" "NotStarted" "Starting" "Preparing" "Running" "Finalizing")
while [[ " ${running[@]} " =~ " ${status} " ]]; do
  echo "Job Status: $status"
  echo "Job URI: $job_uri"
  sleep 8
  status=$(az ml job show -n "$run_id" --query status -o tsv)
  if [[ -z "$status" ]]; then
    echo "Error: Failed to retrieve job status."
    exit 4
  fi
done

# ===========================================
# CHECK FINAL JOB STATUS AND EXIT ACCORDINGLY
# ===========================================
if [[ "$status" == "Completed" ]]; then
  echo "Job completed successfully."
  exit 0
elif [[ "$status" == "Failed" ]]; then
  echo "Job failed."
  exit 1
else
  echo "Job not completed or failed. Status is $status"
  exit 2
fi
