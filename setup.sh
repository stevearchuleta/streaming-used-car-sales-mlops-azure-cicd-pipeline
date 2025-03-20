#!/bin/bash

# =================================================================================
# AZURE ML SETUP SCRIPT FOR MLOPS PIPELINES
# =================================================================================
# Installs the Azure ML CLI extension and sets up default workspace configurations.
# =================================================================================

# ==============================
# INSTALL AZURE ML CLI EXTENSION
# ==============================
echo "Installing Azure ML CLI extension..."
az extension add -n ml -y

# ======================================================
# SET UP DEFAULT RESOURCE GROUP, LOCATION, AND WORKSPACE
# ======================================================
GROUP="default_resource_group_test"  # ==== DEFAULT RESOURCE GROUP ====
LOCATION="westus2"  # ==== DEFAULT AZURE LOCATION ====
WORKSPACE="my_test_workspace"  # ==== DEFAULT AZURE ML WORKSPACE ====

# ===================================
# CHECK IF RESOURCE GROUP NAME EXISTS
# ===================================
RESOURCE_GROUP_NAME=${RESOURCE_GROUP_NAME:-}
if [[ -z "$RESOURCE_GROUP_NAME" ]]
then
    echo "No resource group name [RESOURCE_GROUP_NAME] specified, defaulting to ${GROUP}."
    
    # ========================
    # CONFIGURE AZURE DEFAULTS
    # ========================
    echo "Configuring Azure ML defaults..."
    az configure --defaults group=$GROUP workspace=$WORKSPACE location=$LOCATION
    echo "Default resource group set to $GROUP"
else
    echo "Workflows are using the new subscription."
fi
