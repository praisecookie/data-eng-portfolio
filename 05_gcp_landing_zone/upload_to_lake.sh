#!/bin/bash

# ==========================================
# Data Lake Ingestion Script
# ==========================================

# 1. Define Variables
BUCKET_NAME="gs://cookielou-data-lake-landing" 

# We are going to upload the dirty data from Project 4
SOURCE_FILE="../04_local_etl/dirty_customers.csv"

# We use $(date) to dynamically stamp the upload time
echo "Starting data ingestion to GCP at $(date)"

# 2. Upload the file using Google Cloud Storage CLI
# We are copying it into a virtual folder called /landing_zone/
echo "Uploading $SOURCE_FILE to $BUCKET_NAME/landing_zone/..."
gcloud storage cp $SOURCE_FILE $BUCKET_NAME/landing_zone/

# 3. Verify
echo "Upload complete! Here are the current contents of your Data Lake:"
gcloud storage ls $BUCKET_NAME/landing_zone/