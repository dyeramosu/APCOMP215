#!/bin/bash

echo "Container is running!"

# Authenticate gcloud using service account
#gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
# Set GCP Project Details
#gcloud config set project $GCP_PROJECT

pip install pipenv
pipenv requirements > requirements.txt
pip install -r requirements.txt
git config --global user.name "wschristina"
git config --global user.email "wschristina@gmail.com"
gcsfuse snapnutrition_data_bucket snapnutrition_data_bucket/
python data_labels_processing/labels_processing.py
echo "Container complete!"

#/bin/bash
#pipenv shell

