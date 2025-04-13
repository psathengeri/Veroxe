gcloud functions deploy validate_file \
  --runtime python310 \
  --trigger-resource ml-dataset-veroxe \
  --trigger-event google.storage.object.finalize \
  --entry-point validate_file \
  --source data-pipeline/cloud-function-validate \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=mlops-veroxe,PUBSUB_TOPIC=data-upload-topic
