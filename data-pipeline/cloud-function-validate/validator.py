import os
from google.cloud import storage
from validator import validate_gcs_file

# Set your bucket name
BUCKET_NAME = "ml-dataset-veroxe"


def validate_file(event, context):
    """Triggered by a change to a file in GCS."""
    file_name = event["name"]
    if not file_name.startswith("uploads/pending/"):
        print(f"Ignored file (not in uploads/pending): {file_name}")
        return

    print(f"Validating file: {file_name}")
    is_valid, errors = validate_gcs_file(BUCKET_NAME, file_name)

    if is_valid:
        # Move to uploads/processed/
        processed_file_name = file_name.replace("uploads/pending/", "uploads/processed/")
        move_blob(BUCKET_NAME, file_name, processed_file_name)
        print(f"✅ File is valid. Moved to {processed_file_name}")
    else:
        print(f"❌ Validation failed for {file_name}")
        for err in errors:
            print(f"  • {err}")


def move_blob(bucket_name, source_blob_name, destination_blob_name):
    """Moves a file within the same bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    source_blob = bucket.blob(source_blob_name)
    bucket.copy_blob(source_blob, bucket, destination_blob_name)
    source_blob.delete()
    print(f"Moved file from {source_blob_name} to {destination_blob_name}")
