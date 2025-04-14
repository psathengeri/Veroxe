import json
import logging
from google.cloud import storage
from jsonschema import validate, ValidationError
from logger import log_validation_error  # Logs to BigQuery

# GCS client
storage_client = storage.Client()

# Configs
SCHEMA_BUCKET = "ml-dataset-veroxe"
SCHEMA_FOLDER = "schemas"
PROCESSED_FOLDER = "uploads/processed"

def load_schema(schema_name: str, client_id: str):
    """Load the JSON schema from the GCS schema folder for a specific client."""
    bucket = storage_client.bucket(SCHEMA_BUCKET)
    schema_path = f"{SCHEMA_FOLDER}/{client_id}/{schema_name}"
    blob = bucket.blob(schema_path)

    schema_str = blob.download_as_text()
    return json.loads(schema_str)

def validate_file(event, context):
    """Triggered by a finalized file in GCS."""
    bucket_name = event['bucket']
    file_name = event['name']

    if not file_name.startswith("uploads/pending/"):
        logging.info(f"Skipping non-pending file: {file_name}")
        return

    client_id = file_name.split("/")[1]
    logging.info(f"Processing file: {file_name} for client: {client_id}")

    # Download the file content
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_contents = blob.download_as_text()

    try:
        json_data = json.loads(file_contents)
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in {file_name}")
        log_validation_error(client_id, file_name, "Invalid JSON", "JSON Decode Error")
        return

    # Assume schema file is named like: sensor_readings.schema.json
    schema_name = file_name.split("/")[-1].replace(".json", ".schema.json")

    try:
        schema = load_schema(schema_name, client_id)
        validate(instance=json_data, schema=schema)
        logging.info(f"Validation passed for {file_name}")

        # Move file to uploads/processed/
        new_blob = bucket.copy_blob(
            blob, bucket, file_name.replace("uploads/pending/", f"{PROCESSED_FOLDER}/")
        )
        blob.delete()
        logging.info(f"Moved {file_name} to {new_blob.name}")

    except ValidationError as ve:
        logging.error(f"Validation failed for {file_name}: {ve.message}")
        log_validation_error(client_id, file_name, "Schema Validation Error", ve.message)

    except Exception as e:
        logging.error(f"Unexpected error processing {file_name}: {str(e)}")
        log_validation_error(client_id, file_name, "Unexpected Error", str(e))
