import os
import json
from google.cloud import storage
from google.cloud import pubsub_v1

# Set your bucket and topic info here
BUCKET_NAME = "ml-dataset-veroxe"
PROCESSED_PREFIX = "uploads/processed/"
PENDING_PREFIX = "uploads/pending/"
PUBSUB_TOPIC = "data-upload-topic"
PROJECT_ID = "mlops-veroxe"

storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

def validate_file(data, context):
    file_name = data["name"]
    if not file_name.startswith(PENDING_PREFIX):
        print(f"Ignoring file outside pending/: {file_name}")
        return

    print(f"Processing file: {file_name}")
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)

    # Basic validations
    if not file_name.endswith(".csv"):
        print(f"Invalid file format: {file_name}")
        return

    if blob.size > 10 * 1024 * 1024:  # Limit: 10MB
        print(f"File too large: {file_name}")
        return

    # Read file content to validate schema
    contents = blob.download_as_text()
    header = contents.split("\n")[0].strip()
    expected_columns = {"id", "timestamp", "value"}  # Example schema
    uploaded_columns = set(header.split(","))

    if not expected_columns.issubset(uploaded_columns):
        print(f"Schema mismatch in {file_name}: {uploaded_columns}")
        return

    # Move to uploads/processed/
    new_name = file_name.replace(PENDING_PREFIX, PROCESSED_PREFIX)
    new_blob = bucket.copy_blob(blob, bucket, new_name)
    blob.delete()

    print(f"File {file_name} moved to {new_name}")

    # Optional: Publish to Pub/Sub
    event_data = {
        "file_name": new_name,
        "bucket": BUCKET_NAME,
        "status": "validated"
    }
    publisher.publish(
        f"projects/{PROJECT_ID}/topics/{PUBSUB_TOPIC}",
        json.dumps(event_data).encode("utf-8"),
    )
    print(f"Published message to Pub/Sub for {new_name}")
